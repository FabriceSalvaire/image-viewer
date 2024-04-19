####################################################################################################
#
# ImageBrowser - ...
# Copyright (C) 2024 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
####################################################################################################

"""Module to implement a Qt Application.

"""

####################################################################################################

__all__ = ['QmlApplication']

####################################################################################################

# import datetime
from pathlib import Path
from typing import Union
import argparse
import logging
import sys
import traceback

# Fixme:
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from QtShim.QtCore import (
    Property, Signal, Slot, QObject,
    Qt, QTimer, QUrl
)
from QtShim.QtGui import QGuiApplication, QIcon
from QtShim.QtQml import qmlRegisterType, QQmlApplicationEngine
# Fixme: PYSIDE-574 qmlRegisterSingletonType and qmlRegisterUncreatableType missing in QtQml
from QtShim.QtQml import qmlRegisterUncreatableType
# from QtShim.QtQuick import QQuickPaintedItem, QQuickView
# from QtShim.QtQuickControls2 import QQuickStyle

from ImageBrowser.Common.ArgparseAction import PathAction
from ImageBrowser.Common.Platform import QtPlatform
from .ApplicationMetadata import ApplicationMetadata
from .ApplicationSettings import ApplicationSettings, Shortcut
from .KeySequenceEditor import KeySequenceEditor
from .QmlImageCollection import QmlImageCollection, QmlImage
# from .Runnable import Worker

from .rcc import ImageBrowserRessource

####################################################################################################

_module_logger = logging.getLogger(__name__)

type PathOrStr = Union[Path, str]

####################################################################################################

class QmlApplication(QObject):

    """Class to implement a Qt QML Application."""

    show_message = Signal(str)   # message
    show_error = Signal(str, str)   # message backtrace

    # Fixme: !!!
    preview_done = Signal(str)
    file_exists_error = Signal(str)
    path_error = Signal(str)

    _logger = _module_logger.getChild('QmlApplication')

    ##############################################

    def __init__(self, application: 'Application') -> None:
        super().__init__()
        self._application = application

    ##############################################

    def notify_message(self, message: str) -> None:
        self.show_message.emit(str(message))

    def notify_error(self, message: str) -> None:
        backtrace_str = traceback.format_exc()
        self.show_error.emit(str(message), backtrace_str)

    ##############################################

    @Property(str, constant=True)
    def application_name(self) -> str:
        return ApplicationMetadata.name

    @Property(str, constant=True)
    def application_url(self) -> str:
        return ApplicationMetadata.url

    @Property(str, constant=True)
    def about_message(self) -> str:
        return ApplicationMetadata.about_message()

    ##############################################

    collection_changed = Signal()

    @Property(QmlImageCollection, notify=collection_changed)
    def collection(self) -> QmlImageCollection:
        # return null if None
        return self._application.collection

    ##############################################

    @Slot('QUrl')
    def load_collection(self, url: QUrl) -> None:
        path = url.toString(QUrl.RemoveScheme)
        self._application.load_collection(path)
        self.collection_changed.emit()

####################################################################################################

# Fixme: why not derive from QGuiApplication ???
class Application(QObject):

    """Class to implement a Qt Application."""

    instance = None

    _logger = _module_logger.getChild('Application')

    scanner_ready = Signal()

    ##############################################

    # Fixme: Singleton

    @classmethod
    def create(cls, *args, **kwargs) -> None:
        if cls.instance is not None:
            raise NameError('Instance exists')
        cls.instance = cls(*args, **kwargs)
        return cls.instance

    ##############################################

    def __init__(self) -> None:
        self._logger.info('Ctor')
        super().__init__()

        QtCore.qInstallMessageHandler(self._message_handler)

        self._parse_arguments()

        self._collection = None
        # Fixme: must be defined before QML
        self.load_collection(self._args.path)

        # For Qt Labs Platform native widgets
        # self._application = QGuiApplication(sys.argv)
        # use QCoreApplication::instance() to get instance
        self._application = QApplication(sys.argv)
        self._application.main = self
        self._init_application()

        self._engine = QQmlApplicationEngine()
        self._qml_application = QmlApplication(self)
        self._application.qml_main = self._qml_application

        self._platform = QtPlatform()
        # self._logger.info('\n' + str(self._platform))

        # self._load_translation()
        self._register_qml_types()
        self._set_context_properties()
        self._load_qml_main()

        # self._run_before_event_loop()

        self._thread_pool = QtCore.QThreadPool()
        self._logger.info("Multithreading with maximum {} threads".format(self._thread_pool.maxThreadCount()))

        QTimer.singleShot(0, self._post_init)

    ##############################################

    @property
    def args(self) -> None:   # Fixme
        return self._args

    @property
    def platform(self) -> QtPlatform:
        return self._platform

    @property
    def settings(self) -> ApplicationSettings:
        return self._settings

    @property
    def qml_application(self) -> QmlImageCollection:
        return self._qml_application

    @property
    def thread_pool(self) -> QtCore.QThreadPool:
        return self._thread_pool

    @property
    def collection(self) -> QmlImageCollection:
        return self._collection

    ##############################################

    def _print_critical_message(self, message: str) -> None:
        # print('\nCritical Error on {}'.format(datetime.datetime.now()))
        # print('-'*80)
        # print(message)
        self._logger.critical(message)

    ##############################################

    def _message_handler(self, msg_type, context, msg) -> None:
        if msg_type == QtCore.QtDebugMsg:
            method = self._logger.debug
        elif msg_type == QtCore.QtInfoMsg:
            method = self._logger.info
        elif msg_type == QtCore.QtWarningMsg:
            method = self._logger.warning
        elif msg_type in (QtCore.QtCriticalMsg, QtCore.QtFatalMsg):
            method = self._logger.critical
            # method = None
        # local_msg = msg.toLocal8Bit()
        # localMsg.constData()
        context_file = context.file
        if context_file is not None:
            file_path = Path(context_file).name
        else:
            file_path = ''
        message = '{1} {3} — {0}'.format(msg, file_path, context.line, context.function)
        if method is not None:
            method(message)
        else:
            self._print_critical_message(message)

    ##############################################

    def _on_critical_exception(self, exception: Exception) -> None:
        message = str(exception) + '\n' + traceback.format_exc()
        self._print_critical_message(message)
        self._qml_application.notify_error(exception)
        # sys.exit(1)

    ##############################################

    def _init_application(self) -> None:
        self._application.setOrganizationName(ApplicationMetadata.organisation_name)
        self._application.setOrganizationDomain(ApplicationMetadata.organisation_domain)
        self._application.setApplicationName(ApplicationMetadata.name)
        self._application.setApplicationDisplayName(ApplicationMetadata.display_name)
        self._application.setApplicationVersion(ApplicationMetadata.version)
        logo_path = ':/icons/logo/logo-256.png'
        self._application.setWindowIcon(QIcon(logo_path))
        QIcon.setThemeName('material')
        self._settings = ApplicationSettings()

    ##############################################

    @classmethod
    def setup_gui_application(self) -> None:
        # https://bugreports.qt.io/browse/QTBUG-55167
        # for path in (
        #         'qt.qpa.xcb.xcberror',
        # ) -> None:
        #     QtCore.QLoggingCategory.setFilterRules('{} = false'.format(path))
        QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        # QQuickStyle.setStyle('Material')

    ##############################################

    def _parse_arguments(self) -> None:
        parser = argparse.ArgumentParser(
            description='ImageBrowser',
        )
        # parser.add_argument(
        #     '--version',
        #     action='store_true', default=False,
        #     help="show version and exit",
        # )
        # Fixme: should be able to start application without !!!
        parser.add_argument(
            'path', metavar='PATH',
            action=PathAction,
            help='collection path',
        )
        parser.add_argument(
            '--dont-translate',
            action='store_true',
            default=False,
            help="Don't translate application",
        )
        parser.add_argument(
            '--watcher',
            action='store_true',
            default=False,
            help='start watcher',
        )
        parser.add_argument(
            '--user-script',
            action=PathAction,
            default=None,
            help='user script to execute',
        )
        parser.add_argument(
            '--user-script-args',
            default='',
            help="user script args (don't forget to quote)",
        )
        self._args = parser.parse_args()

    ##############################################

    def _load_translation(self) -> None:
        if self._args.dont_translate:
            return
        # Fixme: ConfigInstall
        # directory = ':/translations'
        directory = str(Path(__file__).parent.joinpath('rcc', 'translations'))
        locale = QtCore.QLocale()
        self._translator = QtCore.QTranslator()
        if self._translator.load(locale, 'collection-browser', '.', directory, '.qm'):
            self._application.installTranslator(self._translator)
        else:
            raise NameError('No translator for locale {}'.format(locale.name()))

    ##############################################

    def _register_qml_types(self) -> None:
        qmlRegisterType(KeySequenceEditor, 'ImageBrowser', 1, 0, 'KeySequenceEditor')
        qmlRegisterUncreatableType(Shortcut, 'ImageBrowser', 1, 0, 'Shortcut', 'Cannot create Shortcut')
        qmlRegisterUncreatableType(ApplicationSettings, 'ImageBrowser', 1, 0, 'ApplicationSettings', 'Cannot create ApplicationSettings')
        qmlRegisterUncreatableType(QmlApplication, 'ImageBrowser', 1, 0, 'QmlApplication', 'Cannot create QmlApplication')
        qmlRegisterUncreatableType(QmlImageCollection, 'ImageBrowser', 1, 0, 'QmlImageCollection', 'Cannot create QmlImageCollection')
        qmlRegisterUncreatableType(QmlImage, 'ImageBrowser', 1, 0, 'QmlImage', 'Cannot create QmlImage')

    ##############################################

    def _set_context_properties(self) -> None:
        context = self._engine.rootContext()
        context.setContextProperty('application', self._qml_application)
        context.setContextProperty('application_settings', self._settings)

    ##############################################

    def _load_qml_main(self) -> None:
        self._logger.info('Load QML...')
        qml_path = Path(__file__).parent.joinpath('qml')
        # qml_path = 'qrc:///qml'
        self._engine.addImportPath(str(qml_path))
        main_qml_path = qml_path.joinpath('main.qml')
        self._qml_url = QUrl.fromLocalFile(str(main_qml_path))
        # QUrl('qrc:/qml/main.qml')
        self._engine.objectCreated.connect(self._check_qml_is_loaded)
        self._engine.load(self._qml_url)
        self._logger.info('QML loaded')

    ##############################################

    def _check_qml_is_loaded(self, obj, url) -> None:
        # See https://bugreports.qt.io/browse/QTBUG-39469
        if (obj is None and url == self._qml_url):
            sys.exit(-1)

    ##############################################

    def exec_(self) -> None:
        # self._view.show()
        self._logger.info('Start event loop')
        sys.exit(self._application.exec_())

    ##############################################

    def _post_init(self) -> None:
        # Fixme: ui refresh ???
        self._logger.info('post Init...')
        if self._args.watcher:
            self._logger.info('Start watcher')
            self._collection.start_watcher() # QtCore.QFileSystemWatcher(self)
        if self._args.user_script is not None:
            self.execute_user_script(self._args.user_script)
        self._logger.info('Post Init Done')

    ##############################################

    def execute_user_script(self, script_path: str) -> None:
        """Execute an user script provided by file *script_path* in a context where is defined a
        variable *application* that is a reference to the application instance.
        """
        script_path = Path(script_path).absolute()
        self._logger.info('Execute user script:\n  {}'.format(script_path))
        try:
            source = open(script_path).read()
        except FileNotFoundError:
            self._logger.info('File {} not found'.format(script_path))
            sys.exit(1)
        try:
            bytecode = compile(source, script_path, 'exec')
        except SyntaxError as exception:
            self._on_critical_exception(exception)
        try:
            exec(bytecode, {'application': self})
        except Exception as exception:
            self._on_critical_exception(exception)
        self._logger.info('User script done')

    ##############################################

    def load_collection(self, path: str) -> None:
        self._logger.info('Load collection {} ...'.format(path))
        self._collection = QmlImageCollection(path)
        self._logger.info('ImageCollection loaded')

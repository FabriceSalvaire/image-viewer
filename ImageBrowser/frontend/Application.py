####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

"""Module to implement a Qt Application.

"""

####################################################################################################

__all__ = ['Application']

####################################################################################################

# import datetime
from pathlib import Path
# from typing import TYPE_CHECKING
import logging
import os
import signal
import sys
import traceback

_module_logger = logging.getLogger(__name__)

# We use https://github.com/spyder-ide/PySide6 Qt shim
# qtpy as a 100 ms overhead
_module_logger.info("««« Import PySide6...")
# import PySide6
from PySide6 import QtCore
from PySide6.QtCore import (
    qInstallMessageHandler, QtMsgType, QMessageLogContext,
    QTranslator,
    QObject,
    QTimer, QUrl, QThreadPool, QLocale,
)
from PySide6.QtGui import QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication
# from PySide6.QtQuickControls2 import QQuickStyle
_module_logger.info("  PySide6 imported »»»")

_module_logger.info("««« Import frontend modules...")
from .ApplicationMetadata import ApplicationMetadata
from .ApplicationSettings import ApplicationSettings   # , Shortcut
from .QmlApplication import QmlApplication
from .QmlImageCollection import QmlImageCollection
#! from ImageBrowser.library.os.platform import QtPlatform

# if TYPE_CHECKING:
from .ApplicationArgs import ApplicationArgs
_module_logger.info("  Frontend modules imported »»»")

# Load Resources
#! from .rcc import resources
_module_logger.info("««« Load rcc")
from .rcc import ImageBrowserRessource
_module_logger.info("  rcc imported »»»")

####################################################################################################

# _module_logger.info(f"Qt binding is {PySide6.API_NAME} v{QtCore.__version__}")
_module_logger.info(f"Qt binding is PySide6 v{QtCore.__version__}")

type PathOrStr = Union[Path, str]

def _make_module_url() -> list[Path]:
    file_path = Path(__file__)
    return [f'file://{_}/' for _ in [p.parents[1] for p in (file_path, file_path.resolve())]]
_MODULE_URLS = _make_module_url()

####################################################################################################

# Fixme: why not derive from QGuiApplication ???
class Application(QObject):

    """Class to implement a Qt Application."""

    instance = None

    _logger = _module_logger.getChild('Application')

    ##############################################

    # @classmethod
    # def setup_gui_application(self) -> None:
    #     https://bugreports.qt.io/browse/QTBUG-55167
    #     for path in (
    #             'qt.qpa.xcb.xcberror',
    #     ):
    #         QLoggingCategory.setFilterRules('{} = false'.format(path))
    #     QQuickStyle.setStyle('Material')

    ##############################################

    # Fixme: Singleton
    @classmethod
    def create(cls, *args: list, **kwargs: dict) -> 'Application':
        if cls.instance is not None:
            raise NameError('Instance exists')
        cls.instance = cls(*args, **kwargs)
        return cls.instance

    ##############################################

    # Use create to get an instance
    def __init__(self, args: ApplicationArgs) -> None:
        self._logger.info('Ctor')
        super().__init__()

        self._args = args

        self._collection = None
        # Fixme: must be defined before QML
        #! self.load_collection(self._args.path)

        # Interrupt from keyboard (CTRL + C)
        signal.signal(signal.SIGINT, self._signal_handler)

        # WARNING: This can solve a crash issue at startup
        if not self._args.no_qt_message_handler:
            qInstallMessageHandler(self._message_handler)

        # For Qt Labs Platform native widgets
        # self._application = QGuiApplication(sys.argv)
        # use QCoreApplication::instance() to get instance
        self._application = QApplication(sys.argv)
        #! self._application.main = self

        self._init_application()

        # combines a QQmlEngine and QQmlComponent
        # to provide a convenient way to load a single QML file
        self._engine = QQmlApplicationEngine()

        self._qml_application = QmlApplication(self)
        #! self._application.qml_main = self._qml_application

        # Fixme: check overhead
        #! self._platform = QtPlatform()
        # self._logger.info('\n' + str(self._platform))

        self._thread_pool = QThreadPool()
        number_of_threads_max = self._thread_pool.maxThreadCount()
        self._logger.info(f'Multithreading with maximum {number_of_threads_max} threads')

        # self._image_provider = ImageProvider()
        # self._engine.addImageProvider('image', self._image_provider)

        self._translator = None
        #! self._load_translation()
        self._set_context_properties()
        self._load_qml_main()

        # Will be called just after the event loop startup
        QTimer.singleShot(0, self._post_init)

        # if isinstance(self._application, QGuiApplication):
        #     self._view = QQuickView()
        #     self._view.setResizeMode(QQuickView.SizeRootObjectToView)
        #     # self._view.setSource(qml_url)
        #     if self._view.status() == QQuickView.Error:
        #         sys.exit(-1)
        # else:
        #     self._view = None

    ##############################################

    # @property
    # def args(self):
    #     return self._args

    # @property
    # def platform(self) -> QtPlatform:
    #     return self._platform

    @property
    def settings(self) -> ApplicationSettings:
        return self._settings

    @property
    def qml_application(self) -> QmlApplication:
        return self._qml_application

    @property
    def thread_pool(self) -> QThreadPool:
        return self._thread_pool

    # @property
    # def image_provider(self) -> ImageProvider:
    #     return self.image_provider

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

    def _signal_handler(self, sig, frame):
        # Fixme: called when QML window is closed
        #   Qt handler ???
        self._logger.info(f"Catched signal {sig}")

    ##############################################

    def _message_handler(self, msg_type: QtMsgType, context: QMessageLogContext, msg: str) -> None:
        # Fixme: can crash at startup
        # Warning: QML console.log is routed to Debug
        #   Use console.log = console.debug, console.info, console.warn, or console.error
        method = None
        match msg_type:
            case QtMsgType.QtDebugMsg:   # 0
                method = self._logger.debug
            case QtMsgType.QtInfoMsg:   # 4
                method = self._logger.info
            case QtMsgType.QtWarningMsg:   # 1
                method = self._logger.warning
            case QtMsgType.QtCriticalMsg | QtMsgType.QtFatalMsg:   # 2 | 3
                method = self._logger.critical
            case _:
                method = self._logger.critical

        msg = str(msg)
        for _ in _MODULE_URLS:
            msg = msg.replace(_, '')

        # local_msg = msg.toLocal8Bit()
        # localMsg.constData()
        context_file = context.file
        if context_file is not None:
            path = Path(context_file)
            file_path = path.name
            # is_qml = path.suffix == '.qml'
        else:
            file_path = ''
            # is_qml = False

        sep = os.linesep + '  '
        if file_path:
            sep += '  '
        function = f' / {context.function}' if context.function else ''
        message = f'\033[1;34m{file_path}{function}\033[0m{sep}{msg}'   # context.line

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
        # Define Organisation
        self._application.setOrganizationName(ApplicationMetadata.organisation_name)
        self._application.setOrganizationDomain(ApplicationMetadata.organisation_domain)

        # Define Application
        self._application.setApplicationName(ApplicationMetadata.name)
        self._application.setApplicationDisplayName(ApplicationMetadata.display_name)
        self._application.setApplicationVersion(ApplicationMetadata.version)

        # Set logo
        # logo_path = ':/icons/logo/logo-256.png'
        # self._application.setWindowIcon(QIcon(logo_path))

        # Set icon theme
        #  cf. ImageBrowser/frontend/rcc/image-browser.qrc
        #      ImageBrowser/frontend/rcc/icons/material/index.theme
        _ = QIcon.themeSearchPaths()
        self._logger.info(f"Theme search path: {_}")
        _ = QIcon.fallbackThemeName()
        self._logger.info(f"Fallback icon Theme: {_}")
        QIcon.setThemeName('material')
        # ['~/.local/share/icons',
        #  '/var/lib/flatpak/exports/share/icons',
        #  '/usr/share/icons',
        #  '/var/lib/snapd/desktop/icons',
        # ':/icons'
        # ]

        # Settings
        self._settings = ApplicationSettings()

    ##############################################

    def _load_translation(self) -> None:
        if self._args.dont_translate:
            return
        # Fixme: ConfigInstall
        # directory = ':/translations'
        directory = str(Path(__file__).parent.joinpath('rcc', 'translations'))
        locale = QLocale()
        self._translator = QTranslator()
        if self._translator.load(locale, '...', '.', directory, '.qm'):
            self._application.installTranslator(self._translator)
        else:
            raise NameError(f'No translator for locale {locale.name()}')

    ##############################################

    def _set_context_properties(self) -> None:
        context = self._engine.rootContext()
        context.setContextProperty('application', self._qml_application)

    ##############################################

    def _load_qml_main(self) -> None:
        self._logger.info('')
        # Register for QML
        from .KeySequenceEditor import KeySequenceEditor

        qml_path = Path(__file__).parent.joinpath('qml')
        # qml_path = 'qrc:///qml'
        self._engine.addImportPath(str(qml_path))

        main_qml_path = qml_path.joinpath('main.qml')
        self._qml_url = QUrl.fromLocalFile(str(main_qml_path))
        # QUrl('qrc:/qml/main.qml')
        self._engine.objectCreated.connect(self._check_qml_is_loaded)
        self._logger.info('««« Load QML...')
        self._engine.load(self._qml_url)
        self._logger.info('  QML loaded »»»')

    ##############################################

    def _check_qml_is_loaded(self, obj: QObject, url: QUrl) -> None:
        # See https://bugreports.qt.io/browse/QTBUG-39469
        if (obj is None and url == self._qml_url):
            sys.exit(-1)

    ##############################################

    def exec_(self) -> int:
        # if self._view is not None:
        #     self._view.show()
        self._logger.info('Start Qt event loop')
        rc = self._application.exec()
        self._logger.info(f"Qt event loop exited with {rc}")
        # Deleting the view before it goes out of scope is required
        # to make sure all child QML instances are destroyed in the correct order.
        # if self._view is not None:
        #     del self._view
        # destroy QML now, else it will continue to log...
        del self._engine
        return rc

    ##############################################

    def _post_init(self) -> None:
        self._logger.info('««« Post Init...')
        # if self._args.watcher:
        #     self._logger.info('Start watcher')
        #     self._collection.start_watcher()   # QtCore.QFileSystemWatcher(self)
        path = Path(self._args.path)
        if path.exists():
            url = QUrl(f'file:{path}')
            self._qml_application.load_collection(url)
        if self._args.user_script is not None:
            self.execute_user_script(self._args.user_script)
        self._logger.info('  Post Init Done »»»')

    ##############################################

    def execute_user_script(self, script_path: str) -> None:
        """Execute an user script provided by file *script_path* in a context where is defined a
        variable *application* that is a reference to the application instance.

        """
        script_path = Path(script_path).absolute()
        self._logger.info(f'Execute user script:\n  {script_path}')
        try:
            with open(script_path, encoding='utf-8') as fh:
                source = fh.read()
        except FileNotFoundError:
            self._logger.info(f'File {script_path} not found')
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

    def load_collection(self, path: PathOrStr) -> None:
        self._logger.info(f"Load collection {path} ...")
        self._collection = QmlImageCollection(path)
        self._logger.info('ImageCollection loaded')

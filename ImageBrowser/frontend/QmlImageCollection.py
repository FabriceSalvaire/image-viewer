####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = ['QmlImageCollection']

####################################################################################################

from pathlib import Path
import glob
import logging
import subprocess
import time

from PySide6.QtCore import (
    Qt,
    QAbstractListModel,
    QFileSystemWatcher,
    Property, Signal, Slot, QObject,
    QByteArray,
)
from PySide6.QtQml import QmlElement, QmlUncreatable, ListProperty

# Fixme: Linux only
from ImageBrowser.backend.thumbnail.FreeDesktop import ThumbnailCache, ThumbnailSize
from ImageBrowser.backend.ImageCollection.ImageCollection import DirectoryCollection, Image
from .Runnable import Worker

####################################################################################################

QML_IMPORT_NAME = 'ImageBrowser'
QML_IMPORT_MAJOR_VERSION = 1
QML_IMPORT_MINOR_VERSION = 0   # Optional

####################################################################################################

_module_logger = logging.getLogger(__name__)

thumbnail_cache = ThumbnailCache()

####################################################################################################

@QmlElement
@QmlUncreatable('QmlImage')
class QmlImage(QObject):

    _logger = _module_logger.getChild('QmlImage')

    ##############################################

    def __init__(self, qml_collection: 'QmlImageCollection', image: Image) -> None:
        super().__init__()
        self._qml_collection = qml_collection
        self._image = image

    ##############################################

    def __repr__(self) -> str:
        return '{0} {1}'.format(self.__class__.__name__, self._image)

    ##############################################

    @property
    def image(self) -> Image:
        return self._image

    ##############################################

    # Fixme: ???
    path_changed = Signal()

    @Property(str, notify=path_changed)
    def path(self) -> str:
        return self._image.path_str

    name_changed = Signal()

    @Property(str, notify=name_changed)
    def name(self) -> str:
        return self._image.name

    ##############################################

    index_changed = Signal()

    @Property(int, notify=index_changed)
    def index(self) -> int:
        return self._image.index
        # return int(self._image)

    ##############################################

    @Property(int, constant=True)
    def large_thumbnail_size(self) -> int:
        return thumbnail_cache.size_for(ThumbnailSize.LARGE)

    large_thumbnail_path_changed = Signal()

    @Property(str, notify=large_thumbnail_path_changed)
    def large_thumbnail_path(self) -> str:
        # Fixme: cache thumbnail instance ?
        return str(thumbnail_cache[self._image.path].large_path)

    thumbnail_ready = Signal()

    @Slot()
    def request_large_thumbnail(self) -> None:
        # Fixme: async
        def job():
            # Fixme: issue when the application is closed
            return str(thumbnail_cache[self._image.path].large)
        worker = Worker(job)
        worker.signals.finished.connect(self.thumbnail_ready)
        from .Application import Application
        Application.instance.thread_pool.start(worker)

    ##############################################

    @Slot(str)
    def open_in_external_program(self, program: str) -> None:
        command = (program, self.path)
        self._logger.info(' '.join(command))
        process = subprocess.Popen(command)

####################################################################################################

@QmlElement
@QmlUncreatable('QmlImageCollection')
# class QmlImageCollection(QObject):
class QmlImageCollection(QAbstractListModel):

    # Model for QML
    #  - QList<QObject*> provides the properties of the objects in the list as roles

    # QAbstractListModel
    #   Call QAbstractItemModel::dataChanged() when model has changed

    # Sorting
    #  https://doc.qt.io/Qt-6/qml-qtqml-models-sortfilterproxymodel.html

    new_image = Signal(int)

    _logger = _module_logger.getChild('QmlImageCollection')

    ##############################################

    def __init__(self, path: str, parent=None) -> None:
        super().__init__(parent)
        self._collection = DirectoryCollection(path)
        # We must prevent garbage collection
        # iter = self._collection.iter_by_index
        iter = self._collection.iter_by_name
        self._images = [QmlImage(self, image) for image in iter]
        # self.reset()

    ##############################################

    @Property(str, constant=True)
    def path(self) -> str:
        return str(self._collection.path)

    ##############################################

    subdirectories_changed = Signal()

    @Property('QStringList', notify=subdirectories_changed)
    def subdirectories(self) -> list[str]:
        return self._collection.subdirectories

    ##############################################

    number_of_images_changed = Signal()

    @Property(int, notify=number_of_images_changed)
    def number_of_images(self):
        # return self._collection.number_of_images
        return len(self._images)

    @Slot(int, result=bool)
    def is_valid_index(self, index):
        return 0 < index < self.number_of_images

    ##############################################

    last_index_changed = Signal()

    @Property(int, notify=last_index_changed)
    def last_index(self):
        return self._collection.last_index

    ##############################################

    images_changed = Signal()

    # https://doc.qt.io/qtforpython-6/examples/example_qml_tutorials_extending-qml_chapter5-listproperties.html
    # https://doc.qt.io/qtforpython-6/PySide6/QtQml/QQmlListReference.html#PySide6.QtQml.QQmlListReference
    # https://doc.qt.io/qt-6/qqmllistproperty.html
    # https://doc.qt.io/qt-6/qqmllistreference.html
    # ListProperty(QObject, append=None, at=None, count=None, replace=None, clear=None, removeLast=None)

    # @Property(QQmlListProperty, notify=images_changed)
    # def images(self):
    #     return QQmlListProperty(QmlImage, self, self._images)

    def rowCount(self, parent=None) -> int:
        # required by QAbstractListModel
        # _ = len(self._images)
        # self._logger.info(f"= {_}")
        # return _
        return len(self._images)

    # def at(self, index: int) -> QmlImage:
    #     return self._images[index]

    ImageRole = Qt.UserRole + 1

    def roleNames(self):
        # required by QAbstractListModel for QML
        # required by Repeater
        # https://bugreports.qt.io/browse/PYSIDE-2698
        self._logger.info(f"QmlImageCollection ImageRole = {self.ImageRole}")
        return {
            self.ImageRole: QByteArray(b'image...'),
        }
        # default = super().roleNames()
        # default[self.RatioRole] = QByteArray(b"ratio")

    def data(self, index, role: int = Qt.DisplayRole) -> QmlImage:
        # required by QAbstractListModel
        # if role == Qt.DisplayRole:
        _ = index.row()
        # self._logger.info(f"index {_} role {role}")
        return self._images[_]
        # return None

    # @Slot(result=bool)
    # def reset(self) -> bool:
    #     self._logger.info("")
    #     self.beginResetModel()
    #     # self.resetInternalData()  # should work without calling it ?
    #     self.endResetModel()
    #     return True

    # images = ListProperty(
    #     QmlImage,
    #     append=None,
    #     at=at,
    #     count=rowCount,
    #     replace=None,
    #     clear=None,
    #     removeLast=None,
    #     notify=images_changed,
    #     final=True,
    # )

    ##############################################


    @Slot(str)
    def sort(self, key: str) -> None:
        self._logger.info(f"Sort by {key}")

        def _sort(func):
            self.beginResetModel()
            self._logger.info(f"sent beginResetModel")
            self._images.sort(key=func)
            self._logger.info(f"sorting done")
            self.endResetModel()
            self._logger.info(f"sent endResetModel")

        match key:
            case 'index':
                _sort(lambda qml_image: qml_image.image.index)
            case 'name':
                _sort(lambda qml_image: qml_image.image.name)
            case 'mtime':
                _sort(lambda qml_image: qml_image.image.mtime)

    ##############################################

    @Property(QmlImage)
    def first_image(self):
        try:
            return self._images[0]
        except IndexError:
            return None

    @Property(QmlImage)
    def last_image(self):
        try:
            return self._images[-1]
        except IndexError:
            return None

    @Slot(int, result=QmlImage)
    def image(self, index):
        try:
            return self._images[index]
        except IndexError:
            return None

    ##############################################

    # def start_watcher(self, watcher=None):
    #     self._files = set(self._glob_files())
    #     self._watcher = watcher or QFileSystemWatcher()
    #     self._watcher.addPath(str(self._collection.path))
    #     self._watcher.directory_changed.connect(self._on_directory_change)

    ##############################################

    # def _glob_files(self):
    #     pattern = str(self._collection.path.joinpath('*' + self._collection.extension))
    #     for path in glob.glob(pattern):
    #         yield Path(path).name

    ##############################################

    # def _on_directory_change(self, path):
    #     time.sleep(3)
    #     # QTimer::singleShot(200, this, SLOT(updateCaption()));
    #     files = set(self._glob_files())
    #     new_files = files - self._files
    #     self._logger.info('New files {}'.format(new_files))
    #     # Fixme: overwrite
    #     for filename in new_files:
    #         self._on_new_file(filename)
    #     self._files = files

    ##############################################

    # def _on_new_file(self, filename):
    #     self._logger.info('New file {}'.format(filename))
    #     # try:
    #     image = self._collection.add_image(filename)
    #     image._index = self._collection.number_of_images   # Fixme: !!!
    #     self._logger.info('New image\n{}'.format(image))
    #     self._images.append(QmlImage(self, image))
    #     self.number_of_images_changed.emit()
    #     self.new_image.emit(image.index)
    #     # except Exception as exception:
    #     #     self._logger.warning('Error on {}\n{}'.format(filename, exception))

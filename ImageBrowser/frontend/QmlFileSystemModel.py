####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = ['QmlFileSystemModel']

####################################################################################################

# from pathlib import Path
# import glob
import logging

from PySide6.QtCore import (
    Qt,
    QAbstractListModel,
    QFileSystemWatcher,
    Property, Signal, Slot, QObject,
    QByteArray,
    QDir, QAbstractListModel, QFile, QTextStream,
    QMimeDatabase, QFileInfo, QStandardPaths, QModelIndex,
)
from PySide6.QtQml import QmlElement, QmlSingleton, QmlUncreatable
from PySide6.QtWidgets import QFileSystemModel

####################################################################################################

QML_IMPORT_NAME = 'ImageBrowser'
QML_IMPORT_MAJOR_VERSION = 1
QML_IMPORT_MINOR_VERSION = 0   # Optional

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

@QmlElement
# @QmlSingleton
@QmlUncreatable('QmlFileSystemModel')
class QmlFileSystemModel(QFileSystemModel):

    root_index_changed = Signal()

    ##############################################

    def get_default_root_directory():
        return QStandardPaths.writableLocation(QStandardPaths.StandardLocation.HomeLocation)

    ##############################################

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._root_index = QModelIndex()
        self.setFilter(QDir.Filter.AllEntries | QDir.Filter.Hidden | QDir.Filter.NoDotAndDotDot)
        self.set_initial_directory()
        # self.mDb = QMimeDatabase()

    ##############################################

    def columnCount(self, parent):
        # Reimplements
        #   we only need one column in this example
        return 1

    ##############################################

    def set_initial_directory(self, path=get_default_root_directory()):
        dir = QDir(path)
        if dir.makeAbsolute():
            self.setRootPath(dir.path())
        else:
            self.setRootPath(self.get_default_root_directory())
        self._set_root_index(self.index(dir.path()))

    ##############################################

    # Fixme: root_index deosn't work ???

    @Property(QModelIndex, notify=root_index_changed)
    def rootIndex(self):
        return self._root_index

    ##############################################

    # @rootIndex.setter
    def _set_root_index(self, index):
        if (index == self._root_index):
            return
        self._root_index = index
        self.root_index_changed.emit()

    ##############################################

    # # check for the correct mime type and then read the file.
    # # returns the text file's content or an error message on failure
    # @Slot(str, result=str)
    # def readFile(self, path):
    #     if path == "":
    #         return ""

    #     file = QFile(path)

    #     mime = self.mDb.mimeTypeForFile(QFileInfo(file))
    #     if ('text' in mime.comment().lower()
    #             or any('text' in s.lower() for s in mime.parentMimeTypes())):
    #         if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
    #             stream = QTextStream(file).readAll()
    #             file.close()
    #             return stream
    #         else:
    #             return self.tr("Error opening the file!")
    #     return self.tr("File type not supported!")

    # @Slot(QQuickTextDocument, int, result=int)
    # def currentLineNumber(self, textDocument, cursorPosition):
    #     td = textDocument.textDocument()
    #     tb = td.findBlock(cursorPosition)
    #     return tb.blockNumber()

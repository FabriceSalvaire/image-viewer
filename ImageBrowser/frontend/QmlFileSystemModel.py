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

__all__ = ['QmlFileSystemModel']

####################################################################################################

# from pathlib import Path
# import glob
import logging

from qtpy.QtCore import (
    Qt,
    QAbstractListModel,
    QFileSystemWatcher,
    Property, Signal, Slot, QObject,
    QByteArray,
    QDir, QAbstractListModel, QFile, QTextStream,
    QMimeDatabase, QFileInfo, QStandardPaths, QModelIndex,
)
from qtpy.QtQml import QmlElement, QmlSingleton, QmlUncreatable
from qtpy.QtWidgets import QFileSystemModel

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

    rootIndexChanged = Signal()

    ##############################################

    def getDefaultRootDir():
        return QStandardPaths.writableLocation(QStandardPaths.StandardLocation.HomeLocation)

    ##############################################

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.mRootIndex = QModelIndex()
        self.mDb = QMimeDatabase()
        self.setFilter(QDir.Filter.AllEntries | QDir.Filter.Hidden | QDir.Filter.NoDotAndDotDot)
        self.setInitialDirectory()

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

    ##############################################

    def setInitialDirectory(self, path=getDefaultRootDir()):
        dir = QDir(path)
        if dir.makeAbsolute():
            self.setRootPath(dir.path())
        else:
            self.setRootPath(self.getDefaultRootDir())
        self.setRootIndex(self.index(dir.path()))

    ##############################################

    # we only need one column in this example
    def columnCount(self, parent):
        return 1

    ##############################################

    @Property(QModelIndex, notify=rootIndexChanged)
    def rootIndex(self):
        return self.mRootIndex

    ##############################################

    def setRootIndex(self, index):
        if (index == self.mRootIndex):
            return
        self.mRootIndex = index
        self.rootIndexChanged.emit()

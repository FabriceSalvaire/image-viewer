####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__ALL__ = ['QmlPathNavigator']

####################################################################################################

from pathlib import Path
import logging

from PySide6.QtCore import (
    Property, Signal, Slot, QObject,
)
from PySide6.QtQml import QmlElement, QmlUncreatable

####################################################################################################

QML_IMPORT_NAME = 'ImageBrowser'
QML_IMPORT_MAJOR_VERSION = 1
QML_IMPORT_MINOR_VERSION = 0   # Optional

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

@QmlElement
@QmlUncreatable('QmlPathNavigator')
class QmlPathNavigator(QObject):

    _logger = _module_logger.getChild('QmlPathNavigator')

    # path_changed = Signal(Directory)
    path_changed = Signal(str)

    ##############################################

    def __init__(self, path: Path = None, parent=None) -> None:
        super().__init__(parent)
        self._path = None
        if path is not None:
            self.path = Path(path)

    ##############################################

    def _set_path(self, path: Path, emit: bool = True) -> None:
        _ = Path(path)
        if self._path != _:
            self._path = _
            if emit:
                _ = str(self._path)
                self.path_changed.emit(_)

    ##############################################

    @property
    def path(self) -> Path:
        return self._path

    @path.setter
    def path(self, path: Path) -> None:
        self._set_path(path, emit=False)

    ##############################################

    # Fixme: ok Property notify ???

    path_str_changed = Signal()

    @Property(str, notify=path_str_changed)
    def path_str(self) -> str:
        return str(self._path)

    @path_str.setter
    def path_str(self, path: str) -> None:
        self._set_path(path, emit=False)

    # text = Property(str, text, setText, notify=textChanged)

    ##############################################

    path_parts_changed = Signal()

    @Property('QStringList', notify=path_parts_changed)
    def path_parts(self) -> list[str]:
        if self._path is not None:
            return self._path.parents
        else:
            return []

    ##############################################

    # @Slot()
    # def directory_list(self):
    #     directories = sorted([directory.basename() for directory in self._path.XXX()],
    #                          key=lambda x: x.lower())
    #     return directory

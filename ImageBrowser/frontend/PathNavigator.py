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

from ImageBrowser.library.unicode import usorted

####################################################################################################

QML_IMPORT_NAME = 'ImageBrowser'
QML_IMPORT_MAJOR_VERSION = 1
QML_IMPORT_MINOR_VERSION = 0   # Optional

####################################################################################################

_module_logger = logging.getLogger(__name__)

type PathStr = Path | str

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
            self.path = Path(path).absolute()
        self._parent_subdirectories = []

    ##############################################

    def _set_path(self, path: Path, emit: bool = True) -> None:
        print(f"_set_path {path} {emit}")
        _ = Path(path).absolute()
        if self._path != _:
            self._path = _
            if emit:
                _ = str(self._path)
                self.path_changed.emit(_)
                self.path_parts_changed.emit()
                self.path_str_changed.emit()

    ##############################################

    @property
    def path(self) -> Path:
        return self._path

    @path.setter
    def path(self, path: PathStr) -> None:
        self._set_path(path, emit=False)

    ##############################################

    # Fixme: ok Property notify ???

    path_str_changed = Signal()

    @Property(str, notify=path_str_changed)
    def path_str(self) -> str:
        return str(self._path)

    @path_str.setter
    def path_str(self, path: str) -> None:
        self._set_path(path, emit=True)

    # text = Property(str, text, setText, notify=textChanged)

    ##############################################

    path_parts_changed = Signal()

    @Property('QStringList', notify=path_parts_changed)
    def path_parts(self) -> list[str]:
        if self._path is not None:
            return self._path.parts[1:]   # remove /
        else:
            return []

    ##############################################

    def parent_subdirectory(self, part_index: int) -> Path:
        if self._path is not None:
            number_of_parts = len(self._path.parts)
            i = number_of_parts - part_index -2
            return self._path.parents[i]
        else:
            return None

    def list_directory(self, path: Path) -> list[str]:
        try:
            return ([_.name for _ in path.iterdir() if _.is_dir() and not _.name.startswith('.')])
        except FileNotFoundError:
            return []

    parent_subdirectories_changed = Signal()

    @Property('QStringList', notify=parent_subdirectories_changed)
    def parent_subdirectories(self) -> list[str]:
        return self._parent_subdirectories

    # @Slot(int, result='QStringList')
    # def list_parent(self, part_index: int) -> list[str]:
    @Slot(int)
    def set_parent_subdirectory(self, part_index: int) -> None:
        if self._path is not None:
            path = self.parent_subdirectory(part_index)
            _ = self.list_directory(path)
            # print(f"list_parent {part_index}/{number_of_parts} {i} {path}")
            print(f"list_parent {part_index} -> {path}")
            print(f"list_parent {_}")
        else:
            _ = []
        self._parent_subdirectories = _
        self.parent_subdirectories_changed.emit()

    @Slot(int)
    def cd_parent(self, part_index: int) -> None:
        _ = self.parent_subdirectory(part_index)
        self._set_path(_)

    @Slot(int, str)
    def cd_parent_subdirectory(self, part_index: int, directory: str) -> None:
        _ = self.parent_subdirectory(part_index).joinpath(directory)
        self._set_path(_)

    ##############################################

    @Slot(str, result='QStringList')
    def complete(self, partial_path: str) -> list[str]:
        # /..../parent/
        # /..../parent/...
        # print(f'complete {partial_path}')
        path = Path(partial_path)
        if not partial_path.endswith('/'):
            stem = path.stem
            path = path.parent
        else:
            stem = ''
        if path.exists():
            completions = self.list_directory(path)
            if stem:
                completions = [_ for _ in completions if _.startswith(stem)]
            print(f"complete '{partial_path}' = '{path}' / '{stem}' -> {completions}")
            if completions:
                default = completions[0]
                return [str(path.joinpath(default))] + completions
        return []

    @Slot(str, str, result=str)
    def complete_with(self, partial_path: str, directory: str) -> str:
        path = Path(partial_path)
        if not partial_path.endswith('/'):
            path = path.parent
        return str(path.joinpath(directory))

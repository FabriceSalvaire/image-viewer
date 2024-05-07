####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

from pathlib import Path
from typing import List, Union
import os

type PathStr = Union[Path, str]

####################################################################################################

class WalkerAbc:

    """Base class to implement a walk in a file hierarchy."""

    ##############################################

    def __init__(self, path: PathStr) -> None:
        # Make the path absolute, resolving any symlinks.
        self._path = Path(path).expanduser().resolve()
        if not self._path.exists():
            raise ValueError(f"Path {self._path} doesn't exists")

    ##############################################

    @property
    def path(self) -> Path:
        return self._path

    ##############################################

    def run(self,
            top_down: bool = False,
            sort: bool = False,
            follow_links: bool = False,
            max_depth: int = -1,
            ) -> None:
        if max_depth >= 0:
            top_down = True
            depth = 0
        for dirpath, dirnames, filenames in self._path.walk(topdown=top_down, followlinks=follow_links):
            if top_down and sort:
                self.sort_dirnames(dirnames)
            if hasattr(self, 'on_directory'):
                for directory in dirnames:
                    self.on_directory(dirpath, directory)
            if hasattr(self, 'on_filename'):
                for filename in filenames:
                    self.on_filename(dirpath, filename)
            if max_depth >= 0:
                depth += 1
                if depth > max_depth:
                    break

    ##############################################

    def sort_dirnames(self, dirnames: List[str]) -> None:
        dirnames.sort()

    ##############################################

    # def on_directory(self, dirpath: str, dirname: str) -> None:
    #     raise NotImplementedError

    ##############################################

    # def on_filename(self, dirpath: str, filename: str) -> None:
    #     raise NotImplementedError

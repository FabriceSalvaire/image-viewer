####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = ['ImageCollection', 'DirectoryCollection']

####################################################################################################

from pathlib import Path
from typing import Iterator, Union, Callable
import logging
import os

from .Image import Image as ImageAbc

type PathOrStr = Union[Path, str]

####################################################################################################

_module_logger = logging.getLogger(__name__)

LINESEP = os.linesep

####################################################################################################

class Image(ImageAbc):

    _logger = _module_logger.getChild('Image')

    ##############################################

    def __init__(self, collection: 'ImageCollection', path: Path, index: int) -> None:
        super().__init__(path)
        self._collection = collection
        self._index = index

    ##############################################

    @property
    def collection(self) -> 'ImageCollection':
        return self._collection

    @property
    def index(self) -> int:
        return self._index

    ##############################################

    def __repr__(self) -> str:
        return f"{self._path} {self._index}"

    def __int__(self) -> int:
        return self._index

    ##############################################

    def __lt__(self, other: 'Image') -> bool:
        """Sort by index"""
        return int(self) < int(other)

####################################################################################################

class ImageCollection:

    """Class to implement an abstract collection of images"""

    __image_cls__ = Image

    EXTENSIONS = (
        '.png',
        '.jpg',
        '.jpeg',
        '.webp',
        '.tiff',
    )

    _logger = _module_logger.getChild('ImageCollection')

    ##############################################

    def __init__(self) -> None:
        self._images = []

    ##############################################

    def __len__(self) -> int:
        return len(self._images)

    @property
    def number_of_images(self) -> int:
        return len(self._images)

    @property
    def last_index(self) -> int:
        return len(self._images) - 1

    ##############################################

    def __getitem__(self, index) -> Image:
        return self._images[index]

    @property
    def first_image(self) -> Image:
        try:
            return self._images[0]
        except IndexError:
            return None

    @property
    def last_image(self) -> Image:
        try:
            return self._images[-1]
        except IndexError:
            return None

    ##############################################

    def __iter__(self) -> Iterator[Image]:
        return iter(self._images)

    def iter_by(self, key: Callable) -> Iterator[Image]:
        images = list(self._images)
        images.sort(key=key)
        return iter(images)

    def iter_by_index(self) -> Iterator[Image]:
        return self.iter_by(lambda image: int(image))

    def iter_by_mtime(self) -> Iterator[Image]:
        return self.iter_by(lambda image: image.mtime)

    def iter_by_size(self) -> Iterator[Image]:
        return self.iter_by(lambda image: image.size)

    ##############################################

    def add_image(self, path: PathOrStr) -> Image:
        _ = self.__image_cls__(self, path, len(self._images))
        self._images.append(_)
        return _

####################################################################################################

class DirectoryCollection(ImageCollection):

    """Class to implement a directory collection of images"""

    _logger = _module_logger.getChild('DirectoryCollection')

    ##############################################

    def __init__(self, path: PathOrStr) -> None:
        super().__init__()
        self._path = Path(str(path)).resolve()
        self._get_images()

    ##############################################

    @property
    def path(self) -> Path:
        return self._path

    def joinpath(self, name: str) -> Path:
        return self._path.joinpath(str(name))

    ##############################################

    @property
    def _list_dir(self) -> Iterator[str]:
        return self._path.iterdir()

    def _get_images(self) -> None:
        # self._images = []
        for name in self._list_dir:
            path = self.joinpath(name)
            if path.is_dir():
                pass
            elif path.is_file() and path.suffix in self.EXTENSIONS:
                try:
                    self.add_image(path)
                except Exception as e:
                    self._logger.warning(f"Error on {path}{LINESEP}{e}")
        self._images.sort()   # by index

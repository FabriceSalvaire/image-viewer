####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = ['Image']

####################################################################################################

from pathlib import Path
from typing import TYPE_CHECKING
import logging
import os
import stat

import PIL
import numpy as np

import xattr

if TYPE_CHECKING:
    from .ImageCollection import ImageCollection

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Image:

    """Class to implement an image"""

    _logger = _module_logger.getChild('Image')

    ##############################################

    def __init__(self, collection: 'ImageCollection', path: Path, index: int) -> None:
        self._collection = collection
        self._path = Path(path)
        self._index = index
        self._stat = None
        self._size = None
        self._mtime = None
        self._format = None
        self.release_image()
        self._logger.info(repr(self))

    ##############################################

    @property
    def collection(self) -> 'ImageCollection':
        return self._collection

    @property
    def path(self) -> Path:
        return self._path

    @property
    def path_str(self) -> str:
        return str(self._path)

    @property
    def path_bytes(self) -> bytes:
        return bytes(self._path)

    @property
    def name(self) -> str:
        return self._path.name

    @property
    def stem(self) -> str:
        return self._path.stem

    @property
    def suffix(self) -> str:
        return self._path.suffix

    @property
    def index(self) -> int:
        return self._index

    @property
    def shape(self) -> [int, int]:
        if self._image is not None:
            return self._image.shape
        else:
            return None

    ##############################################

    @property
    def is_symlink(self) -> bool:
        return self._path.is_symlink()

    ##############################################

    # https://docs.python.org/3/library/os.html#os.stat_result

    @property
    def stat(self) -> os.stat_result:
        # if not hasattr(self, '_stat'):
        if self._stat is None:
            self._stat = self._path.stat(follow_symlinks=True)
        return self._stat

    @property
    def mtime(self) -> int:
        if self._mtime is None:
            self._mtime = stat.st_mtime_ns
        return self._mtime

    @property
    def size(self) -> int:
        if self._size is None:
            self._size = stat.st_size
        return self._size

    ##############################################

    # Mime type / image format
    # Exif
    # sha

    ##############################################

    def __repr__(self) -> str:
        return f"{self._path} {self._index}"

    def __str__(self) -> str:
        return str(self.path)

    def __int__(self) -> int:
        return self._index

    ##############################################

    def __lt__(self, other: 'Image') -> bool:
        """Sort by index"""
        return int(self) < int(other)

    ##############################################

    def release_image(self) -> None:
        self._image = None

    def _load_image(self, reload: bool = False) -> None:
        if self._image is None or reload:
            # Fixme: implement alternative loader ?
            #   Qt
            pil_image = PIL.Image.open(self.path)
            self._image = np.asarray(pil_image)
            self._format = pil_image.format
            # pil_image.get_format_mimetype()
            # self._logger.info('Image shape {}'.format(self._image.shape))

    @property
    def image(self) -> np.ndarray:
        self._load_image()
        return self._image

    ##############################################

    USER_BALOO_RATING = 'user.baloo.rating'

    @property
    def rating(self) -> int:
        path = self.path_bytes
        if self.USER_BALOO_RATING in xattr.listxattr(path):
            _ = xattr.getxattr(path, self.USER_BALOO_RATING)
            return int(_)
        else:
            return -1

    @rating.setter
    def rating(self, rating: int) -> None:
        path = self.path_bytes
        _ = str(rating).encode('ascii')
        xattr.setxattr(path, self.USER_BALOO_RATING, _)

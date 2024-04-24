####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

"""Module to implement freedesktop.org thumbnail cache
https://specifications.freedesktop.org/thumbnail-spec/thumbnail-spec-latest.html

The thumbnails directory have the following internal structure:
- $XDG_CACHE_HOME/thumbnails/
- $XDG_CACHE_HOME/thumbnails/normal
- $XDG_CACHE_HOME/thumbnails/large/
- $XDG_CACHE_HOME/thumbnails/x-large/
- $XDG_CACHE_HOME/thumbnails/xx-large/
- $XDG_CACHE_HOME/thumbnails/fail/

"""

####################################################################################################

__all__ = ['ThumbnailCache']

####################################################################################################

from enum import IntEnum, auto
from pathlib import Path
from typing import Union
import hashlib
import logging
import mimetypes
# import shutil

from PIL import Image, PngImagePlugin

from ImageBrowser.common.Singleton import SingletonMetaClass

####################################################################################################

_module_logger = logging.getLogger(__name__)

type PathOrStr = Union(Path, str)

####################################################################################################

class ThumbnailSize(IntEnum):
    NORMAL = 0
    LARGE = auto()
    X = auto()
    XX = auto()
    FAIL = auto()

####################################################################################################

class ThumbnailCache(metaclass=SingletonMetaClass):

    """Class to import  Thumbnail Cache"""

    PATHS = ('normal', 'large', 'x-large', 'xx-large', 'fail')
    SIZES = (128, 256, 512, 1024, 0)

    _logger = _module_logger.getChild('ThumbnailCache')

    ##############################################

    @classmethod
    def size_for(cls, size: ThumbnailSize) -> int:
        return cls.SIZES[size]

    ##############################################

    def __init__(self) -> None:
        self._path = Path.home().joinpath('.cache', 'thumbnails')
        self._size_path = tuple([self._path.joinpath(_) for _ in self.PATHS])
        for _ in self._size_path:
            _.mkdir(parents=True, exist_ok=True)

    ##############################################

    @property
    def path(self) -> Path:
        return self._path

    def path_for(self, size: ThumbnailSize) -> Path:
        return self._size_path[size]

    @property
    def normal_path(self) -> Path:
        return self._size_path[ThumbnailSize.NORMAL]

    @property
    def large_path(self) -> Path:
        return self._size_path[ThumbnailSize.LARGE]

    @property
    def x_path(self) -> Path:
        return self._size_path[ThumbnailSize.X]

    @property
    def xx_path(self) -> Path:
        return self._size_path[ThumbnailSize.XX]

    @property
    def fail_path(self) -> Path:
        return self._size_path[ThumbnailSize.FAIL]

    ##############################################

    def clear_cache(self) -> None:
        # Warning: This command is dangerous !!!
        # self._logger.info('Clear thumbnail cache {}'.format(self._path))
        # shutil.rmtree(str(self._path), ignore_errors=True)
        pass

    ##############################################

    def thumbnail_path_for(self, path: PathOrStr, size: ThumbnailSize) -> Path:
        return self.path_for(size).joinpath(path)

    def normal_thumbnail_path(self, path: PathOrStr) -> Path:
        return self.thumbnail_path_for(path, ThumbnailSize.NORMAL)

    def large_thumbnail_path(self, path: PathOrStr) -> Path:
        return self.thumbnail_path_for(path, ThumbnailSize.LARGE)

    def x_thumbnail_path(self, path: PathOrStr) -> Path:
        return self.thumbnail_path_for(path, ThumbnailSize.X)

    def xx_thumbnail_path(self, path: PathOrStr) -> Path:
        return self.thumbnail_path_for(path, ThumbnailSize.XX)

    ##############################################

    def __getitem__(self, path: PathOrStr) -> 'Thumbnail':
        return Thumbnail(self, path)

####################################################################################################

class Thumbnail:

    IMAGE_FORMAT = 'png'
    IMAGE_EXTENSION = '.' + IMAGE_FORMAT
    SAMPLING = Image.BICUBIC

    _logger = _module_logger.getChild('Thumbnail')

    ##############################################

    @classmethod
    def add_uri(cls, path: PathOrStr) -> str:
        return 'file://' + str(path)

    ##############################################

    @classmethod
    def mangle_path(cls, path: PathOrStr) -> str:
        uri = cls.add_uri(path)
        return hashlib.md5(uri.encode('utf-8')).hexdigest() + cls.IMAGE_EXTENSION

    ##############################################

    def __init__(self, cache: ThumbnailCache, path: PathOrStr) -> None:
        self._cache = cache
        self._source_path = Path(path).resolve()
        self._filename = self.mangle_path(path)
        self._stat = self._source_path.stat()

    ##############################################

    @property
    def source_path(self) -> Path:
        return self._source_path

    @property
    def uri(self) -> str:
        return self.add_uri(self._source_path)

    ##############################################

    @property
    def size(self) -> int:
        return self._stat.st_size

    @property
    def mtime(self) -> int:
        return int(self._stat.st_mtime_ns)

    @property
    def mime_type(self):
        return mimetypes.guess_type(str(self._source_path))[0]

    ##############################################

    def thumbnail_path(self, size: ThumbnailSize) -> Path:
        return self._cache.thumbnail_path_for(self._filename, size)

    @property
    def normal_path(self) -> Path:
        return self._cache.normal_thumbnail_path(self._filename)

    @property
    def large_path(self) -> Path:
        return self._cache.large_thumbnail_path(self._filename)

    @property
    def x_path(self) -> Path:
        return self._cache.x_thumbnail_path(self._filename)

    @property
    def xx_path(self) -> Path:
        return self._cache.xx_thumbnail_path(self._filename)

    ##############################################

    def _delete_thumbnail(self, size: ThumbnailSize) -> None:
        _ = self.thumbnail_path(size)
        if _.exists():
            self._logger.info(f"Delete thumbnail for {self._source_path}")
            _.unlink(missing_ok=True)

    def delete_thumbnail(self) -> None:
        for _ in ThumbnailSize:
            self._delete_thumbnail(_)

    ##############################################

    def has_thumbnail(self, size: ThumbnailSize) -> bool:
        # Fixme: compare the original file's size and modification time
        #        with the attribytes stored in the 'Thumb::MTime' and 'Thumb::Size' keys
        #   if ((!thumb.isShared && !isSet(thumb.MTime)) ||
        #       (isSet(thumb.MTime) && file.mtime != thumb.MTime) ||
        #       (isSet(thumb.Size) && file.size != thumb.Size) {
        #     recreate_thumbnail();
        #   }
        path = self.thumbnail_path(size)
        if path.exists():
            stat = path.stat()
            size = int(stat.st_size)
            mtime = int(stat.st_mtime)   # Fixme: int ???
            if not size or mtime < self.mtime:
                self.delete_thumbnail()
            else:
                return True
        return False

    def has_normal_thumbnail(self, path: PathOrStr) -> bool:
        return self.has_thumbnail(ThumbnailSize.NORMAL)

    def has_large_thumbnail(self, path: PathOrStr) -> bool:
        return self.has_thumbnail(ThumbnailSize.LARGE)

    def has_x_thumbnail(self, path: PathOrStr) -> bool:
        return self.has_thumbnail(ThumbnailSize.X)

    def has_xx_thumbnail(self, path: PathOrStr) -> bool:
        return self.has_thumbnail(ThumbnailSize.XX)

    ##############################################

    def _make_png_info(self) -> PngImagePlugin.PngInfo:
        # {
        #     'Thumb::URI': 'file:///home/fabrice/....png'
        #     'Thumb::MTime': '1547660783',
        #
        #     'Thumb::Size': '3312888',
        #     'Thumb::Mimetype': 'image/png',
        #     'Software': 'KDE Thumbnail Generator Images (GIF, PNG, BMP, ...)',
        #
        #     'dpi': (96, 96),
        # }
        png_info = PngImagePlugin.PngInfo()
        # required
        png_info.add_text('Thumb::URI', self.uri)
        png_info.add_text('Thumb::MTime', str(self.mtime))
        # optional
        png_info.add_text('Thumb::Size', str(self.size))
        png_info.add_text('Thumb::Mimetype', self.mime_type)
        # Description
        png_info.add_text('Software', 'ImageBrowser')
        # Thumb::Image::Width
        # Thumb::Image::Height
        # Thumb::Movie::Length
        return png_info

    ##############################################

    def _make_thumbnail(self, dst_path: Path, size: int) -> None:
        # Fixme:
        #  async
        #  convert
        #  atomic rename tmp
        image = Image.open(str(self._source_path))
        image.thumbnail((size, size), resample=self.SAMPLING)
        png_info = self._make_png_info()
        image.save(str(dst_path), 'PNG', pnginfo=png_info)

    ##############################################

    def _make_thumbnail_for(self, size: ThumbnailSize) -> None:
        self._make_thumbnail(self.thumbnail_path(size), self._cache.size_for(size))

    ##############################################

    def thumbnail(self, size: ThumbnailSize) -> Path:
        # Fixme: mangle x3
        if not self.has_thumbnail(size):
            self._logger.info(f"Make thumbnail for {self._source_path}")
            self._make_thumbnail_for(size)
        return self.thumbnail_path(size)

    @property
    def normal(self) -> Path:
        return self.thumbnail(ThumbnailSize.NORMAL)

    @property
    def large(self) -> Path:
        return self.thumbnail(ThumbnailSize.LARGE)

    @property
    def x(self) -> Path:
        return self.thumbnail(ThumbnailSize.X)

    @property
    def xx(self) -> Path:
        return self.thumbnail(ThumbnailSize.XX)

####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

"""**Design Note**

On Linux, filenames are just a bunch of bytes, and are not necessarily encoded in a particular
encoding.  Python 3 tries to turn everything into Unicode strings, and implements a scheme to
translate byte strings to Unicode strings and back without loss, and without knowing the original
encoding.  Python3 uses partial surrogates to encode the 'bad' bytes, but the normal UTF8 encoder
can't handle them when printing to the terminal.

Example::

    # decode
    bad_utf8 = b'C\xc3N'.decode('utf8','surrogateescape')
    # encode
    bad_utf8.encode('utf8','surrogateescape')
    # but UnicodeEncodeError: 'utf-8' codec can't encode character ...
    print(bad_utf8)

"""

####################################################################################################

__all__ = ['File']

DANGEROUS = True

####################################################################################################

from pathlib import Path
from typing import AnyStr, Optional, Type, Union
import hashlib
import logging
import os
import subprocess

import xattr

####################################################################################################

_module_logger = logging.getLogger(__name__)

LINESEP = os.linesep

type PathStr = Union[Path, str]

####################################################################################################

class File:

    ST_NBLOCKSIZE = 512

    __slots__ = [
        '_path',
        '_stat',
        '_allocated_size',
        '_sha',
        'user_data',
    ]

    SHA_METHOD = hashlib.sha1

    SOME_BYTES_SIZE = 64    # rdfind uses 64
    PARTIAL_SHA_BYTES = 10 * 1024

    _logger = _module_logger.getChild('File')

    ##############################################

    def __init__(self, *path: list[PathStr], resolve: bool = True, strict: bool = False) -> None:
        # Fixme: typing
        _ = Path(*path)
        if resolve:
            # Return a new path with expanded ~ and ~user constructs
            _ = _.expanduser()
            # Make the path absolute, resolving any symlinks.
            # If the path doesn’t exist and strict is True, FileNotFoundError is raised.
            _ = _.resolve(strict)
        self._path = _
        self.vacuum()

    ##############################################

    def vacuum(self) -> None:
        self._stat = None
        self._allocated_size = None
        self._sha = None
        self.user_data = None

    ##############################################

    # pathlib API

    @property
    def path(self) -> Path:
        return self._path

    @property
    def path_str(self) -> Path:
        return str(self._path)

    def __str__(self) -> str:
        return str(self._path)

    @property
    def parent(self) -> str:
        return self._path.parent

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
    def exists(self) -> bool:
        return self._path.exists()

    @property
    def is_file(self) -> bool:
        return self._path.is_file()

    @property
    def is_symlink(self) -> bool:
        return self._path.is_symlink()

    ##############################################

    # Stat API

    @property
    def stat(self) -> os.stat_result:
        # if not hasattr(self, '_stat'):
        if self._stat is None:
            self._stat = self._path.stat(follow_symlinks=False)
        return self._stat

    @property
    def is_empty(self) -> bool:
        return self.stat.st_size == 0

    @property
    def size(self) -> int:
        return self.stat.st_size

    @property
    def inode(self) -> int:
        return self.stat.st_ino

    @property
    def device(self) -> int:
        return self.stat.st_dev

    @property
    def mtime(self) -> int:
        return self.stat.st_mtime_ns

    @property
    def uid(self) -> int:
        return self.stat.st_uid

    @property
    def gid(self) -> int:
        return self.stat.st_gid


    @property
    def allocated_size(self) -> int:
        # See https://raw.githubusercontent.com/coreutils/coreutils/master/src/du.c
        # https://github.com/rofl0r/gnulib/blob/master/lib/stat-size.h
        # define ST_NBLOCKSIZE 512
        # ST_NBLOCKS (*sb) * ST_NBLOCKSIZE
        # if not hasattr(self, '_allocated_size'):
        if self._allocated_size is None:
            self._allocated_size = self.stat.st_blocks * 512
        return self._allocated_size

    ##############################################

    def read(self, size: Optional[int] = None) -> bytes:
        # unlikely to happen
        # if self.is_empty:
        #     return b''
        with open(self._path, 'rb') as fh:
            if size is not None and size < 0:
                if abs(size) < self.size:
                    fh.seek(size, os.SEEK_END)
                    size = abs(size)
                else:
                    size = None
            data = fh.read(size)
        return data

    ##############################################

    @property
    def sha(self) -> str:
        if self._sha is None:
            if self.is_empty:
                self._sha = ''
            else:
                data = self.read()
                self._sha = self.SHA_METHOD(data).hexdigest()
        return self._sha

    ##############################################

    def partial_sha(self, size: Optional[int] = None) -> str:
        if self.is_empty:
            return ''
        if size is None:
            size = self.PARTIAL_SHA_BYTES
        data = self.read(size)
        return self.SHA_METHOD(data).hexdigest()

    ##############################################

    def first_bytes(self, size: Optional[int] = None) -> bytes:
        if size is None:
            size = self.SOME_BYTES_SIZE
        return self.read(size)

    def last_bytes(self, size: Optional[int] = None) -> bytes:
        if size is None:
            size = self.SOME_BYTES_SIZE
        return self.read(-size)

    ##############################################

    def compare_with(self, other: 'File', posix: bool = False) -> bool:
        if posix:
            return self._compare_with_posix(other)
        return self._compare_with_py(other)


    def _compare_with_posix(self, other: 'File') -> bool:
        # Fixme: portability
        command = ('/usr/bin/cmp', '--silent', str(self), str(other))
        # Fixme: check ?
        return subprocess.run(command).returncode == 0


    def _compare_with_py(self, other: 'File') -> bool:
        size = self.size
        if size != other.size:
            return False

        # Fixme: check < CHUNK_SIZE, > CHUNK_SIZE, = CHUNK_SIZE +1, ...
        CHUNK_SIZE = 1024
        with open(self.path_bytes, 'rb') as fh1:
            with open(other.path_bytes, 'rb') as fh2:
                offset = 0
                while offset < size:
                    offset += CHUNK_SIZE
                    fh1.seek(offset)
                    fh2.seek(offset)
                    data1 = fh1.read(CHUNK_SIZE)
                    data2 = fh2.read(CHUNK_SIZE)
                    if data1 != data2:
                        return False
            return True

    ##############################################

    def is_identical_to(self, other: 'File'):
        return (
            not self.is_empty
            and self.size == other.size
            and self.first_bytes == other.first_bytes
            and self.last_bytes == other.last_bytes
            and (self.size <= self.PARTIAL_SHA_BYTES or self.partial_sha() == other.partial_sha())
            and self.sha == other.sha
            and self.compare_with(other)
        )

    ##############################################

    def _find_rename_alternative(self, dst: Path, pattern: str) -> Path:
        parent = dst.parent
        stem = dst.stem
        suffix = dst.suffix
        i = 0
        while True:
            i += 1
            new_dst = parent / pattern.format(stem=stem, i=i, suffix=suffix)
            if not new_dst.exists():
                return new_dst

    ##############################################

    def delete(self) -> None:
        self._logger.info(f"delete{LINESEP}{self}")
        # Danger !
        # if DANGEROUS:
        #!!! self._path.unlink()

    ##############################################

    def rename(self, dst: PathStr,
               pattern: str = "{stem} ({i}){suffix}",
               rebuild: bool = False
               ) -> Type['File'] | None:
        if isinstance(dst, str):
            dst = Path(dst)
        if dst == self.path:
            self._logger.warning(f"same destination{self}")
            return None
        if dst.exists():
            new_dst = self._find_rename_alternative(dst, pattern)
            self._logger.warning(f"{dst} exists, rename {self} to {new_dst}")
            dst = new_dst
        # recheck
        if dst.exists():
            raise NameError(f"Internal Error: {dst} exists")
        self._logger.info(f"rename{LINESEP}{self}{LINESEP}  ->{LINESEP}{dst}")
        # Danger !
        if DANGEROUS:
            self.path.rename(dst)
        if rebuild:
            return self.from_path(dst)
        else:
            return dst

    ##############################################

    def move_to(self, dst: PathStr) -> None:
        dst_path = Path(dst) / self.name
        self._logger.info(f"move{LINESEP}{self}{LINESEP}  ->{LINESEP}{dst_path}")
        self.rename(dst_path)

    ##############################################

    def write(self, data: bytes) -> None:
        with open(self._path, 'wb') as fh:
            fh.write(data)

    ##############################################

    # Fixme: portability
    #   Linux only

    USER_BALOO_RATING = 'user.baloo.rating'

    @property
    def rating(self) -> int:
        path = str(self)
        if self.USER_BALOO_RATING in xattr.listxattr(path):
            _ = xattr.getxattr(path, self.USER_BALOO_RATING)
            return int(_)
        else:
            return -1

    @rating.setter
    def rating(self, rating: int) -> None:
        path = str(self)
        _ = str(rating).encode('ascii')
        xattr.setxattr(path, self.USER_BALOO_RATING, _)

####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = ['FileImage']

####################################################################################################

from pathlib import Path
import logging

import numpy as np

from ImageBrowser.path.file import File
from .ImageLoader import ImageLoader

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class ImageAbc:

    """Class to implement an image"""

    _logger = _module_logger.getChild('ImageAbc')

    ##############################################

    def __init__(self) -> None:
        self._image = None

    ##############################################

    @property
    def size(self) -> int:
        raise NotImplementedError

    ##############################################

    def release_image(self) -> None:
        self._image = None

    def load_image(self) -> None:
        raise NotImplementedError

    @property
    def image(self) -> np.ndarray:
        self.load_image()
        return self._image

    @property
    def shape(self) -> [int, int]:
        if self._image is not None:
            return self._image.shape
        else:
            return None


####################################################################################################

class NpImage(ImageAbc):

    _logger = _module_logger.getChild('NpImage')

    ##############################################

    def __init__(self, path: Path) -> None:
        ImageAbc.__init__(self)

    ##############################################

    def load_image(self, image) -> None:
        self._image = np.asarray(image)

####################################################################################################

class FileImage(ImageAbc, File):

    _logger = _module_logger.getChild('FileImage')

    # Fixme: set default loader ???

    ##############################################

    def __init__(self, path: Path) -> None:
        File.__init__(self, path)
        ImageAbc.__init__(self)
        self._logger.info(repr(self))

    ##############################################

    def load_image(self, loader: ImageLoader, reload: bool = False) -> None:
        if self._image is None or reload:
            self._image = loader.load(self._path)
            #! self._format = pil_image.format
            # pil_image.get_format_mimetype()
            # self._logger.info('Image shape {}'.format(self._image.shape))

####################################################################################################

class RemoteImage(ImageAbc):

    _logger = _module_logger.getChild('RemoteImage')

    ##############################################

    def __init__(self, url: str) -> None:
        ImageAbc.__init__(self)
        self._url = str(url)

    ##############################################

    @property
    def url(self) -> str:
        return self._str

    ##############################################

    # Def load_image(self, loader: ImageLoader, reload: bool = False) -> None:
    #     if self._image is None or reload:
    #         self._image = loader.load(self._path)

####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = ['ImageLoader']

####################################################################################################

import logging
from pathlib import Path
from typing import Union

import numpy as np

####################################################################################################

_module_logger = logging.getLogger(__name__)

type PathStr = Union[Path, str]

####################################################################################################

class ImageLoader:

    ##############################################

    def __init__(self) -> None:
        pass

    ##############################################

    def load(self, path: PathStr) -> np.ndarray:
        meth = self.pil_loader
        return meth(path)

    ##############################################

    def pil_loader(self, path: PathStr) -> np.ndarray:
        _ = str(path)
        import PIL
        _ = PIL.Image.open(_)
        return np.asarray(_)

    ##############################################

    def cv_loader(self, path: PathStr) -> np.ndarray:
        _ = str(path)
        import cv2 as cv
        return cv.imread(_)

    ##############################################

    def qt_loader(self, path: PathStr) -> np.ndarray:
        _ = str(path)
        from PySide6.QtGui import QImage
        img = QImage(_)
        width = img.width()
        height = img.height()
        ptr = img.constBits()
        _ = np.array(ptr)
        # Fixme: 4 for RGBA format
        _ = _.reshape(height, width, 4)
        return _

    ##############################################

    # remote image require a network manager
    # to handle protocol, auth, header ...

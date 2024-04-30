####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = [
    'Shortcuts',
    'ExternalProgram',
]

####################################################################################################

from pathlib import Path

from PySide6.QtCore import QCoreApplication

from ImageBrowser.config import ConfigInstall

####################################################################################################

class Shortcuts:
    previous_image = QCoreApplication.translate('shortcut', 'Previous image'), 'Backspace'
    next_image = QCoreApplication.translate('shortcut', 'Next image'), 'n'   # Space
    flip_image = QCoreApplication.translate('shortcut', 'Flip image'), 'r'
    fit_to_screen = QCoreApplication.translate('shortcut', 'Fit to screen'), 'f'
    full_zoom = QCoreApplication.translate('shortcut', 'Full Zoom'), 'z'
    # open_image_in_external_program = QCoreApplication.translate('shortcut', 'Open in External Program'), ''
    # apply_filter_on_image = QCoreApplication.translate('shortcut', 'Apply Filter on Image'), ''

####################################################################################################

class ExternalProgram:

    if ConfigInstall.OS.on_linux:
        gimp = Path('/usr', 'bin', 'gimp')

    else:
        gimp = None

    default = gimp

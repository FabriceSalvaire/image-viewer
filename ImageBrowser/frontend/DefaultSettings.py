####################################################################################################
#
# ImageBrowser - ...
# Copyright (C) 2024 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
####################################################################################################

__all__ = [
    'Shortcuts',
    'ExternalProgram',
]

####################################################################################################

from pathlib import Path

from qtpy.QtCore import QCoreApplication

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

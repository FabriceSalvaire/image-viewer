####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

"""Module to implement argparse actions.

"""

####################################################################################################

__all__ = ['PathAction']

####################################################################################################

import argparse
from pathlib import Path

####################################################################################################

class PathAction(argparse.Action):

    """Class to implement argparse action for path."""

    ##############################################

    def __call__(self, parser, namespace, values, option_string=None) -> Path:
        if values is not None:
            if isinstance(values, list):
                path = [Path(_) for _ in values]
            else:
                path = Path(values)
        else:
            path = None
        setattr(namespace, self.dest, path)

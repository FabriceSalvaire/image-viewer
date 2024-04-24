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

__all__ = [
    'PathAction',
]

####################################################################################################

import argparse
from pathlib import Path

####################################################################################################

class PathAction(argparse.Action):

    """Class to implement argparse action for path."""

    ##############################################

    def __call__(self, parser, namespace, values, option_string=None):

        if values is not None:
            if isinstance(values, list):
                path = [Path(x) for x in values]
            else:
                path = Path(values)
        else:
            path = None
        setattr(namespace, self.dest, path)

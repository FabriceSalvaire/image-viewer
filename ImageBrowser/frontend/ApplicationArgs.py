####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

"""Module to implement a Qt Application.

"""

####################################################################################################

__all__ = ['ApplicationArgs']

####################################################################################################

from pathlib import Path
import argparse

from ImageBrowser.library.args import PathAction

####################################################################################################

class ApplicationArgs:

    ##############################################

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(
            description='ImageBrowser',
        )

        parser.add_argument(
            '--no-qt-message-handler',
            action='store_true',
            default=False,
            help="don't install Qt message handler (This can solve a crash issue at startup)",
        )

        # parser.add_argument(
        #     '--version',
        #     action='store_true', default=False,
        #     help="show version and exit",
        # )
        # Fixme: should be able to start application without !!!

        parser.add_argument(
            'path', metavar='PATH',
            action=PathAction,
            help='collection path',
        )

        parser.add_argument(
            '--dont-translate',
            action='store_true',
            default=False,
            help="Don't translate application",
        )

        parser.add_argument(
            '--user-script',
            action=PathAction,
            default=None,
            help='user script to execute',
        )

        parser.add_argument(
            '--user-script-args',
            default='',
            help="user script args (don't forget to quote)",
        )

        parser.add_argument(
            '--logging-level',
            default='INFO',
            # default='DEBUG',
            help="",
        )

        # parser.add_argument(
        #     '--watcher',
        #     action='store_true',
        #     default=False,
        #     help='start watcher',
        # )

        self._args = parser.parse_args()

    ##############################################

    def __getattr__(self, name: str) -> bool | str | int | Path:
        return getattr(self._args, name)

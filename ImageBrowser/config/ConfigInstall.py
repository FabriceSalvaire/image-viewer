####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = ['Path', 'Logging']

####################################################################################################

from pathlib import Path as plPath
import logging
import sys

# due to Path class
from ImageBrowser.library.path.find import find

####################################################################################################

logger = logging.getLogger('root.main')
logger.info(f"Load {__name__}")

####################################################################################################

class OsFactory:

    ##############################################

    def __init__(self) -> None:
        if sys.platform.startswith('linux'):
            self._name = 'linux'
        elif sys.platform.startswith('win'):
            self._name = 'windows'
        elif sys.platform.startswith('darwin'):
            self._name = 'osx'

    ##############################################

    @property
    def name(self) -> str:
        return self._name

    @property
    def on_linux(self) -> bool:
        return self._name == 'linux'

    @property
    def on_windows(self) -> bool:
        return self._name == 'windows'

    @property
    def on_osx(self) -> bool:
        return self._name == 'osx'


OS = OsFactory()

####################################################################################################

_this_file = plPath(__file__).resolve()

class Path:
    module_directory = _this_file.parents[1]
    config_directory = _this_file.parent

####################################################################################################

class Logging:

    default_config_file = 'logging.yml'
    directories = (Path.config_directory,)

    ##############################################

    @staticmethod
    def find(config_file: str) -> plPath:
        return find(config_file, Logging.directories)

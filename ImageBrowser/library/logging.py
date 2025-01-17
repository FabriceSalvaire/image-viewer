####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

"""This subpackage implements logging facilities.

"""

####################################################################################################

__all__ = ['setup_logging']

####################################################################################################

from pathlib import Path
from typing import Optional
import logging
import logging.config
import os
import sys

import yaml

from ImageBrowser.config import ConfigInstall

####################################################################################################

LEVEL_ENV = 'ImageBrowserLogLevel'
APPLICATION_NAME = 'ImageBrowser'

def setup_logging(
    application_name: str = APPLICATION_NAME,
    config_file: str | Path = ConfigInstall.Logging.default_config_file,
    logging_level: Optional[int] = None,
) -> logging.Logger:

    config_file = Path(config_file)
    if not config_file.exists():
        config_file = ConfigInstall.Logging.find(str(config_file))
    with open(config_file, 'r', encoding='utf8') as fh:
        logging_config = yaml.load(fh, Loader=yaml.SafeLoader)

    # Fixme: \033 is not interpreted in YAML
    if ConfigInstall.OS.on_linux:
        formatter_config = logging_config['formatters']['ansi']['format']
        logging_config['formatters']['ansi']['format'] = formatter_config.replace('<ESC>', '\033')

    # Use "simple" formatter for Windows and OSX
    # and "ansi" for Linux
    if ConfigInstall.OS.on_windows or ConfigInstall.OS.on_osx:
        formatter = 'simple'
    else:
        formatter = 'ansi'
    logging_config['handlers']['console']['formatter'] = formatter

    # Load YAML settings
    logging.config.dictConfig(logging_config)

    # Customise logging level
    logger = logging.getLogger(application_name)
    if logging_level is None and LEVEL_ENV in os.environ:
        level_name = os.environ[LEVEL_ENV]
        try:
            logging_level = getattr(logging, level_name.upper())
        except AttributeError:
            sys.exit(f'{LEVEL_ENV} environment variable is set to an invalid logging level "{level_name}"')
    if logging_level:
        # level can be int or string
        logger.setLevel(logging_level)
    # else use logging.yml

    logger.info(f"Loaded {config_file}")
    level = {
        logging.NOTSET: 'NOTSET',
        logging.DEBUG: 'DEBUG',
        logging.INFO: 'INFO',
        logging.WARNING: 'WARNING',
        logging.ERROR: 'ERROR',
        logging.CRITICAL: 'CRITICAL',
    }[logger.level]
    logger.info(f"Level is {level}")

    return logger

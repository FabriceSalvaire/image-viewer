####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

from ImageBrowser import setup_logging
setup_logging()

import logging

import os
# os.environ['PYSIDE67_OPTION_PYTHON_ENUM'] = '1'
os.environ['QT_API'] = 'pyside6'
os.environ['QT_LOGGING_RULES'] = ';'.join((
'*.debug=true',
'qt.*.debug=false',
'*.info=true',
))

from ImageBrowser.frontend.Application import Application

####################################################################################################

def main() -> None:
    logging.info('Start ...')
    # application = Application()
    Application.setup_gui_application()
    application = Application.create()
    application.exec_()

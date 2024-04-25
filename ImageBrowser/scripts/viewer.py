####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__ALL__ = ['main']

# Notice: ImageBrowser.__init__.py and .script are imported first

def main() -> None:
    # early logger
    import logging
    logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        format=logging_format,
        level=logging.INFO,
    )
    logger = logging.getLogger('root.main')
    # logger.propagate = False
    # logger.setLevel(logging.INFO)
    # stream = logging.StreamHandler()
    # stream.setLevel(logging.INFO)
    # formatter = logging.Formatter(logging_format)
    # stream.setFormatter(formatter)
    # logger.addHandler(stream)
    logger.info('Start...')

    # parse args to perform early configurations
    from ImageBrowser.frontend.ApplicationArgs import ApplicationArgs
    args = ApplicationArgs()

    from ImageBrowser.library.logging import setup_logging
    logger = setup_logging(logging_level=args.logging_level)

    import os

    # setup Qt logging
    _ = ';'.join((
        '*.debug=true',
        'qt.*.debug=false',
        '*.info=true',
    ))
    logging.info(f'Set QT_LOGGING_RULES="{_}"')
    os.environ['QT_LOGGING_RULES'] = _

    # setup qtpy
    logging.info('Use PySide6')
    # os.environ['PYSIDE67_OPTION_PYTHON_ENUM'] = '1'
    os.environ['QT_API'] = 'pyside6'

    # import Qt...
    logging.info('Import Application...')
    from ImageBrowser.frontend.Application import Application

    # Application.setup_gui_application()
    application = Application.create(args)
    application.exec_()

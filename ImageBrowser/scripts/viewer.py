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
    # to init startup time
    import logging

    # start global timer
    from ImageBrowser.library.timer import TimerManager
    timer_manager = TimerManager.global_instance()
    startup_timer = timer_manager.new('startup')
    global_timer = timer_manager.new('global')

    # early logger
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
    logging.info(f"logging level: {args.logging_level}")
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
    #   some code imports directly PySide6 !
    logging.info('Use PySide6')
    # os.environ['PYSIDE67_OPTION_PYTHON_ENUM'] = '1'
    os.environ['QT_API'] = 'pyside6'

    # import Qt...
    logging.info('Import Application...')
    from ImageBrowser.frontend.Application import Application
    import sys

    # Application.setup_gui_application()
    application = Application.create(args)
    startup_timer.stop()
    logger.info(f"Startup time {startup_timer.delta_ms:.3f} ms")
    rc = application.exec_()
    global_timer.stop()
    logger.info(f"Global time {global_timer.delta_s:.3f} s")
    logger.info(f"Bye exit with {rc}")
    sys.exit(rc)

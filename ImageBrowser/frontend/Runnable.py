####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

# Code inspired from
#  https://www.twobitarcade.net/article/multithreading-pyqt-applications-with-qthreadpool

####################################################################################################

__all__ = ['Worker']

####################################################################################################

import logging
import traceback

####################################################################################################

from qtpy.QtCore import QRunnable
# from qtpy.QtQml import QQmlListProperty
from qtpy.QtCore import (
    Property, Signal, Slot, QObject,
    Qt, QTimer, QUrl
)

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class WorkerSignals(QObject):

    """Class to define the signals available from a running worker thread.

    .. note:: signals can only be defined on objects derived from QObject.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    progress
         int

    """

    finished = Signal()
    error = Signal(tuple)
    result = Signal(str) # Fixme: object
    progress = Signal(int)

####################################################################################################

class Worker(QRunnable):

    """Class to implement a worker thread.

    .. note:: non-GIL-releasing Python code can only execute in one thread at a time.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    """

    _logger = _module_logger.getChild('Worker')

    ##############################################

    def __init__(self, callback, *args, **kwargs):
        super().__init__()
        self._callback = callback
        self._args = args
        self._kwargs = kwargs
        self._signals = WorkerSignals()

    ##############################################

    @property
    def signals(self):
        return self._signals

    ##############################################

    @Slot()
    def run(self):
        self._logger.info('run {}({}, {})'.format(self._callback, self._args, self._kwargs))
        try:
            result = self._callback(
                *self._args, **self._kwargs,
                # status=self._signals.status,
                # progress=self._signals.progress,
            )
        except:
            traceback.print_exc()
            # exctype, value = sys.exc_info()[:2]
            self._logger.info('emit error')
            # Fixme:
            self._signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self._logger.info('emit result {}'.format(result))
            self._signals.result.emit(result)
        finally:
            self._logger.info('emit finished')
            self._signals.finished.emit()

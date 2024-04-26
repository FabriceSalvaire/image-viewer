####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

"""This module implements timers.
"""

####################################################################################################

__all__ = ['Timer', 'TimerNs', 'TimerManager']

####################################################################################################

from time import time_ns, perf_counter, perf_counter_ns

####################################################################################################

class TimerMixin:

    # Fixme: define time func for start/stop

    ##############################################

    def __init__(self, name: str, start: bool = True) -> None:
        self._name = str(name)
        self._start = None
        self._stop = None
        if start:
            self.reset()

    ##############################################

    @property
    def name(self) -> str:
        return self._name

####################################################################################################

class TimerNs(TimerMixin):

    ##############################################

    def start(self):
        self._stop = None
        self._start = perf_counter_ns()

    def stop(self):
        self._stop = perf_counter_ns()

    ##############################################

    @property
    def delta_ns(self) -> int:
        if self._stop is not None:
            return self._stop - self._start
        return None

    @property
    def delta_ms(self) -> float:
        return self.delta_ns / 1000

    @property
    def delta_s(self) -> float:
        return self.delta_ns / 1000_000

####################################################################################################

class Timer(TimerMixin):

    ##############################################

    def start(self):
        self._stop = None
        self._start = perf_counter()

    def stop(self):
        self._stop = perf_counter()

    ##############################################

    @property
    def delta_s(self) -> float:
        if self._stop is not None:
            return self._stop - self._start
        return None

    @property
    def delta_ms(self) -> float:
        return self.delta_s * 1000

####################################################################################################

class TimerManager:

    GLOBAL_INSTANCE = None

    ##############################################

    @classmethod
    def global_instance(cls) -> 'TimerManager':
        if cls.GLOBAL_INSTANCE is None:
            cls.GLOBAL_INSTANCE = cls()
        return cls.GLOBAL_INSTANCE

    ##############################################

    def __init__(self) -> None:
        self._timers = {}

    ##############################################

    def new(self, name: str, start: bool = True, ns: bool = False) -> Timer:
        if name in self._timers:
            raise NameError(f"Timer {name} already exists")
            # return self._timers[name]
        if ns:
            cls = TimerNs
        else:
            cls = Timer
        _ = cls(name, start=False)
        self._timers[name] = _
        if start:
            _.start()
        return _

    ##############################################

    def __getitem__(self, name: str) -> Timer:
        return self._timers[name]

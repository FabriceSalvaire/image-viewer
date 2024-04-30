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

from datetime import timedelta
from time import time_ns, perf_counter, perf_counter_ns

####################################################################################################

class TimerMixin:

    # Fixme: define time func for start/stop

    ##############################################

    # Fixme: overflow

    @staticmethod
    def ns2us(x: int | float) -> float:
        return x / 1000

    @staticmethod
    def ns2ms(x: int | float) -> float:
        return x / 1000_000

    @staticmethod
    def ns2s(x: int | float) -> float:
        return x / 1000_000_000

    @staticmethod
    def s2ms(x: int | float) -> float:
        return x * 1000

    @staticmethod
    def s2us(x: int | float) -> float:
        return x * 1000_000

    @staticmethod
    def s2ns(x: int | float) -> float:
        return x * 1000_000_000

    ##############################################

    def __init__(self, name: str, start: bool = True) -> None:
        self._name = str(name)
        self._start = None
        self._stop = None
        self._accumulator = 0
        if start:
            self.start()

    ##############################################

    @property
    def name(self) -> str:
        return self._name

    ##############################################

    @property
    def raw_delta(self) -> int | float:
        if self._stop is not None:
            return self._stop - self._start
        return None

    @property
    def delta(self) -> timedelta:
        return timedelta(milliseconds=self.delta_ms)

    ##############################################

    def accumulate(self) -> None:
        self._accumulator += self.raw_delta

    @property
    def raw_accumulator(self) -> int | float:
        return self._accumulator

    @property
    def accumulator(self) -> timedelta:
        return timedelta(milliseconds=self.accumulator_ms)

####################################################################################################

class TimerNs(TimerMixin):

    # Fixme: overflow, run perf_counter in parallel to detect that ?

    ##############################################

    def start(self):
        self._stop = None
        self._start = perf_counter_ns()

    def stop(self):
        self._stop = perf_counter_ns()

    ##############################################

    @property
    def delta_ns(self) -> int:
        return self.raw_delta

    @property
    def delta_us(self) -> float:
        return self.ns2us(self.raw_delta)

    @property
    def delta_ms(self) -> float:
        return self.ns2ms(self.raw_delta)

    @property
    def delta_s(self) -> float:
        return self.ns2s(self.raw_delta)

    ##############################################

    @property
    def accumulator_ns(self) -> int:
        return self.raw_accumulator

    @property
    def accumulator_us(self) -> float:
        return self.ns2us(self.raw_accumulator)

    @property
    def accumulator_ms(self) -> float:
        return self.ns2ms(self.raw_accumulator)

    @property
    def accumulator_s(self) -> float:
        return self.ns2s(self.raw_accumulator)

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
        return self.raw_delta

    @property
    def delta_ms(self) -> float:
        return self.s2ms(self.raw_delta)

    @property
    def delta_us(self) -> float:
        return self.s2us(self.raw_delta)

    ##############################################

    @property
    def accumulator_s(self) -> float:
        return self.raw_accumulator

    @property
    def accumulator_ms(self) -> float:
        return self.s2ms(self.raw_accumulator)

    @property
    def accumulator_us(self) -> float:
        return self.s2us(self.raw_accumulator)

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

####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = [
    'TimeStamp',
    'TimeStampMixin',
]

####################################################################################################

from atomiclong import AtomicLong

####################################################################################################

class TimeStamp:

    """Class to implement timestamp"""

    _time_stamp = AtomicLong(0)

    ##############################################

    def __init__(self):
        self._modified_time = 0

    ##############################################

    def __repr__(self):
        return 'TS {}'.format(self._modified_time)

    ##############################################

    def __lt__(self, other):
        return self._modified_time < other.modified_time

    ##############################################

    def __gt__(self, other):
        return self._modified_time > other.modified_time

    ##############################################

    def __int__(self):
        return self._modified_time

    ##############################################

    def modified(self):

        # Should be atomic
        TimeStamp._time_stamp += 1
        self._modified_time = TimeStamp._time_stamp.value

####################################################################################################

class TimeStampMixin:

    """Mixin to add timestamp to an object"""

     ##############################################

    def __init__(self):
        self._modified_time = TimeStamp()

    ##############################################

    @property
    def modified_time(self):
        return int(self._modified_time)

    ##############################################

    def modified(self):
        self._modified_time.modified()

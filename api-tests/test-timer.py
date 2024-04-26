####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

from time import sleep

from ImageBrowser.library.timer import TimerManager

gt = TimerManager.global_instance()

_ = gt.new('timer_ns', ns=True)
_.stop()
print(f"{_.delta_ns} ns")

for t in (.1, 1, 10, 100, 1000):
    _ = gt.new(f'timer{t}')
    sleep(t / 1000)   # s
    _.stop()
    print(f"{_.delta_ms:.3f} ms vs {t}")

####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

from ImageBrowser.library.logging import setup_logging
from ImageBrowser.library.os.linux import MountPoints

setup_logging()

mounts = MountPoints()
# _ = MountPoints()
rule = '\u2500' * 100
print(rule)
for _ in mounts:
    print(_)
print(rule)

_ = mounts.device_for(__file__)
print(f"device for {__file__} is {_}")

####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

# http://www.pyinvoke.org

####################################################################################################

from invoke import task, Collection
# import sys

####################################################################################################

# SOURCE_PATH = Path(__file__).resolve().parent

####################################################################################################

from . import clean
from . import doc
from . import qt
from . import icon

ns = Collection()
# Fixme: find generic code somewhere ...
ns.add_collection(Collection.from_module(clean))
ns.add_collection(Collection.from_module(doc))
ns.add_collection(Collection.from_module(qt))
ns.add_collection(Collection.from_module(icon))

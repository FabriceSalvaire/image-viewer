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

from . import clean
from . import doc
from . import release

ns = Collection()
ns.add_collection(Collection.from_module(clean))
ns.add_collection(Collection.from_module(release))
ns.add_collection(Collection.from_module(doc))

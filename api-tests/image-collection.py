####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

from pathlib import Path

from ImageBrowser.library.logging import setup_logging
logger = setup_logging()

from ImageBrowser.backend.ImageCollection.ImageCollection import DirectoryCollection
from ImageBrowser.backend.thumbnail.FreeDesktop import ThumbnailCache, ThumbnailSize

####################################################################################################

thumbnail_cache = ThumbnailCache()

# path = Path('~/__priv__').expanduser()
path = Path('./fake-images').absolute()

collection = DirectoryCollection(path)

# for image in collection:
#     print(image)

print('-'*100)
print("By index:")
for image in collection.iter_by_index():
    print('-'*50)
    print(image)
    th = thumbnail_cache[image.path]
    print(th.normal_path)

print()
print('-'*100)
print("By mtime:")
for image in collection.iter_by_mtime():
    print('-'*50)
    print(image)
    th = thumbnail_cache[image.path]
    print(th.normal_path)

print()
print('-'*100)
print('Subdirectories:')
for name in collection.subdirectories:
    print(name)

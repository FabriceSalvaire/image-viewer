####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = ['find']
# , 'expand_path', 'walk'

####################################################################################################

import os
# from pathlib import Path
# from typing import Iterator

####################################################################################################

def find(file_name: str, directories: bytes | list[str]) -> str:
    # Fixme: bytes / str ???
    if isinstance(directories, bytes):
        directories = (directories,)
    for directory in directories:
        for directory_path, _, file_names in directory.walk():
            if file_name in file_names:
                return os.path.join(directory_path, file_name)
    raise NameError(f"File {file_name} not found in directories {str(directories)}")

####################################################################################################

# def expand_path(path: str) -> Path:
#     _ = os.path.expandvars(path)
#     return Path(_).expanduser().absolute()

####################################################################################################

# def walk(path: str, followlinks: bool = False) -> Iterator[Path]:
#     for root, _, files in os.walk(path, followlinks=followlinks):
#         for filename in files:
#             yield Path(root).joinpath(filename)

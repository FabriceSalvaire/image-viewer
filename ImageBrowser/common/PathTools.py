####################################################################################################
#
# ImageBrowser - ...
# Copyright (C) 2024 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
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

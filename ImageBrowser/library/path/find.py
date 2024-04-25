####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

__all__ = ['find']

####################################################################################################

from pathlib import Path

####################################################################################################

def find(file_name: str, directories: str | list[str]) -> Path:
    # Fixme: iterable
    if isinstance(directories, (str, Path)):
        directories = (directories,)
    for _ in directories:
        directory = Path(_)
        for directory_path, _, file_names in directory.walk():
            if file_name in file_names:
                return Path(directory_path, file_name)
    raise NameError(f"File {file_name} not found in directories {str(directories)}")

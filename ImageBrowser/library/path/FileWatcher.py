####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

####################################################################################################

__all__ = ['file_watcher']

####################################################################################################

from pathlib import Path
import logging
import os

from .Singleton import SingletonMetaClass

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class FileWatcher(metaclass=SingletonMetaClass):

    ##############################################

    def __init__(self):
        self._rename_queue = []
        self._delete_queue = []

    ##############################################

    def _push_rename(self, old, new):
        self._rename_queue.append((old, new))

    def _push_delete(self, path):
        self._delete_queue.append(path)

    ##############################################

    def pop_rename(self):
        return self._rename_queue.pop()

    def pop_delete(self):
        return self._delete_queue.pop()

    ##############################################

    def delete_file(self, path, dry_run=False):
        _module_logger.info('Delete\n  {}'.format(path))
        if not dry_run:
            os.unlink(path)
            self._push_delete(path)

    ##############################################

    def rename_file(self, old_path, new_path, dry_run=False):
        old_path = str(old_path)
        new_path = str(new_path)
        _module_logger.info('Rename\n  {}\n->\n{}'.format(old_path, new_path))
        if Path(new_path).exists():
            _module_logger.warning('Cannot rename file: file exists\n{}'.format(new_path))
            return False
        else:
            if not dry_run:
                os.rename(old_path, new_path)
                self._push_rename(old_path, new_path)
            return True

####################################################################################################

# Fixme: versus singleton
file_watcher = FileWatcher()

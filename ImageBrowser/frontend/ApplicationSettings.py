####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

"""Module to implement a application settings.

"""

####################################################################################################

__all__ = [
    'ApplicationSettings',
    'Shortcut',
]

####################################################################################################

from typing import Iterator
import logging

from qtpy.QtCore import (
    Property, Signal, Slot, QObject,
    QSettings,
)
from qtpy.QtQml import QmlElement, QmlUncreatable, ListProperty

from . import DefaultSettings
from .DefaultSettings import Shortcuts

####################################################################################################

QML_IMPORT_NAME = 'ImageBrowser'
QML_IMPORT_MAJOR_VERSION = 1
QML_IMPORT_MINOR_VERSION = 0   # Optional

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

@QmlElement
@QmlUncreatable('Shortcut')
class Shortcut(QObject):

    _logger = _module_logger.getChild('Shortcut')

    ##############################################

    def __init__(
        self,
        settings: DefaultSettings,
        name: str,
        display_name: str,
        sequence: str,
    ) -> None:
        super().__init__()
        self._settings = settings
        self._name = name
        self._display_name = display_name
        self._default_sequence = sequence
        self._sequence = sequence

    ##############################################

    def __repr__(self) -> str:
        return f"Shortcut '{self._name}' '{self._display_name}' '{self._sequence}'"

    ##############################################

    @Property(str, constant=True)
    def name(self) -> str:
        return self._name

    @Property(str, constant=True)
    def display_name(self) -> str:
        return self._display_name

    @Property(str, constant=True)
    def default_sequence(self) -> str:
        return self._default_sequence

    ##############################################

    sequence_changed = Signal()

    @Property(str, notify=sequence_changed)
    def sequence(self) -> str:
        self._logger.info('get sequence {} = {}'.format(self._name, self._sequence))
        return self._sequence

    @sequence.setter
    def sequence(self, value: str) -> str:
        if self._sequence != value:
            self._logger.info('Shortcut {} = {}'.format(self._name, value))
            self._sequence = value
            self._settings.set_shortcut(self)
            self.sequence_changed.emit()

####################################################################################################

@QmlElement
@QmlUncreatable('ApplicationSettings')
class ApplicationSettings(QSettings):

    """Class to implement application settings."""

    _logger = _module_logger.getChild('ApplicationSettings')

    ##############################################

    def __init__(self) -> None:
        # Fixme: file doesn't exists
        super().__init__()
        self._logger.info('Loading settings from {}'.format(self.fileName()))
        self._shortcut_map = {
            name: Shortcut(self, name, self._shortcut_display_name(name), self._get_shortcut(name))
            for name in self._shortcut_names
        }
        self._shortcuts = list(self._shortcut_map.values())
        for _ in self._shortcuts:
            self._logger.info(f"{_}")

    ##############################################

    @property
    def _shortcut_names(self) -> Iterator[str]:
        for name in dir(Shortcuts):
            if not name.startswith('_'):
                yield name

    def _shortcut_display_name(self, name) -> str:
        return getattr(Shortcuts, name)[0]

    def _default_shortcut(self, name) -> str:
        return getattr(Shortcuts, name)[1]

    ##############################################

    def _shortcut_path(self, name) -> str:
        return 'shortcut/{}'.format(name)

    ##############################################

    def _get_shortcut(self, name) -> str:
        path = self._shortcut_path(name)
        if self.contains(path):
            return self.value(path)
        else:
            return self._default_shortcut(name)

    ##############################################

    def set_shortcut(self, shortcut) -> None:
        path = self._shortcut_path(shortcut.name)
        self.setValue(path, shortcut.sequence)

    ##############################################

    # @Property(QQmlListProperty, constant=True)
    # def shortcuts(self) -> QQmlListProperty:
    #     return QQmlListProperty(Shortcut, self, self._shortcuts)

    ##############################################

    @Slot(str, result=Shortcut)
    def shortcut(self, name: str) -> str:
        return self._shortcut_map.get(name, None)

    ##############################################

    # @Slot(str, result=str)
    # def shortcut_sequence(self, name) -> None:
    #     shortcut = self._shortcut_map.get(name, None)
    #     if shortcut is not None:
    #         return shortcut.sequence
    #     else:
    #         return None

    ##############################################

    external_program_changed = Signal()

    __EXTERNAL_PROGRAM_ID__ = 'external_program'

    @Property(str, constant=True)
    def default_external_program(self) -> str:
        # return QUrl('file://' + )
        return str(DefaultSettings.ExternalProgram.default)

    @Property(str, notify=external_program_changed)
    def external_program(self) -> str:
        if self.contains(self.__EXTERNAL_PROGRAM_ID__):
            return self.value(self.__EXTERNAL_PROGRAM_ID__)
        else:
            return self.default_external_program

    @external_program.setter
    def external_program(self, value) -> None:
        self._logger.info('set external sequence {}'.format(value))
        if value != self.external_program:
            self._logger.info('set external sequence {}'.format(value))
            self.setValue(self.__EXTERNAL_PROGRAM_ID__, value)
            self.external_program_changed.emit()

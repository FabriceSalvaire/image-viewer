####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

"""Module to implement a Qt Application.

"""

####################################################################################################

__all__ = ['QmlApplication']

####################################################################################################

from pathlib import Path
from typing import Union, TYPE_CHECKING
import logging
import traceback

from PySide6.QtCore import (
    Property, Signal, Slot, QObject,
    QUrl
)
from PySide6.QtQml import QmlElement, QmlUncreatable

from .ApplicationMetadata import ApplicationMetadata
from .QmlImageCollection import QmlImageCollection
from .QmlFileSystemModel import QmlFileSystemModel
from .PathNavigator import QmlPathNavigator

if TYPE_CHECKING:
    from .Application import Application

####################################################################################################

QML_IMPORT_NAME = 'ImageBrowser'
QML_IMPORT_MAJOR_VERSION = 1
QML_IMPORT_MINOR_VERSION = 0   # Optional

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

@QmlElement
@QmlUncreatable('QmlApplication')
class QmlApplication(QObject):

    """Class to implement a Qt QML Application."""

    show_message = Signal(str)   # message
    show_error = Signal(str, str)   # message backtrace

    # Fixme: !!!
    preview_done = Signal(str)
    file_exists_error = Signal(str)
    path_error = Signal(str)

    _logger = _module_logger.getChild('QmlApplication')

    ##############################################

    def __init__(self, application: 'Application') -> None:
        super().__init__()
        self._application = application
        self._file_system_model = QmlFileSystemModel()
        self._path_navigator = QmlPathNavigator(path=Path.cwd())

    ##############################################

    def notify_message(self, message: str) -> None:
        self.show_message.emit(str(message))

    def notify_error(self, message: str) -> None:
        backtrace_str = traceback.format_exc()
        self.show_error.emit(str(message), backtrace_str)

    ##############################################

    @Property(str, constant=True)
    def application_name(self) -> str:
        return ApplicationMetadata.name

    @Property(str, constant=True)
    def application_url(self) -> str:
        return ApplicationMetadata.url

    @Property(str, constant=True)
    def about_message(self) -> str:
        return ApplicationMetadata.about_message()

    ##############################################

    @Property(QmlFileSystemModel, constant=True, final=True)
    def file_system_model(self) -> QmlFileSystemModel:
        return self._file_system_model

    @Property(QmlPathNavigator, constant=True, final=True)
    def path_navigator(self) -> QmlPathNavigator:
        return self._path_navigator

    ##############################################

    collection_changed = Signal()

    @Property(QmlImageCollection, notify=collection_changed)
    def collection(self) -> QmlImageCollection:
        # return null if None
        return self._application.collection

    ##############################################

    @Slot('QUrl')
    def load_collection(self, url: QUrl) -> None:
        # path = url.toString(QUrl.RemoveScheme)
        path = url.toLocalFile()
        self._logger.info(f"{url}  {path}")
        self._application.load_collection(path)
        self.collection_changed.emit()

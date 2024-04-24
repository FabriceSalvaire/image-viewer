/***************************************************************************************************
 *
 * ImageBrowser — ...
 * Copyright (C) 2024 Fabrice SALVAIRE
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 **************************************************************************************************/

// Fixme: reset, validation, entered

import QtQuick 2.11
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11
import Qt.labs.platform 1.1

import Widgets 1.0 as Widgets

Row {

    /******************************************************
     *
     * API
     *
     */

    property string path

    /*****************************************************/

    id: root

    function set_path(path) {
        // path is prefixed by file://
        if (typeof path === 'object') {
            var prefix = 'file://'
            path = path.toString()
            if (path.startsWith(prefix))
                path = path.slice(prefix.length, path.length)
        }
        if (path)
	    root.path = path
    }

    /******************************************************
     *
     * Dialogs
     *
     */

    FileDialog {
        // Fixme: we cannot set the current file
	id: file_dialog
	fileMode : FileDialog.OpenFile
	onAccepted: set_path(file)
    }

    /******************************************************/

    Widgets.TextField {
        id: text_field
	width: parent.width - button.width
        text: root.path
        // Fixme: validator
        onEditingFinished: set_path(text)
    }

    ToolButton {
	id: button
	icon.name: 'folder-black'
	onClicked: file_dialog.open() // Fixme: current
    }
}

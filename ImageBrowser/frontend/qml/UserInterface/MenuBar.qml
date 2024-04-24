/***************************************************************************************************
 *
 * ImageBrowser — ...
 * Copyright (C) 2024 Fabrice SALVAIRE
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 **************************************************************************************************/

import QtQml 2.2
import QtQuick 2.11
import QtQuick.Controls 2.4

import ImageBrowser 1.0

MenuBar {
    id: root

    /*******************************************************
     *
     * API
     *
     */

    property var about_dialog
    property var collection_folder_dialog
    property var options_dialog
    // application_window.close_application()

    /******************************************************/

    Action {
        id: toggle_menu_bar_action
        shortcut: 'm'
        onTriggered: visible = !visible
    }

    /******************************************************/

    Menu {
        title: qsTr('File')

        // onClosed: xxx.forceActiveFocus()

        Action {
            text: qsTr('Open a collection')
            onTriggered: collection_folder_dialog.open()
        }

        MenuSeparator { }

        MenuItem {
            icon.name: 'settings-black'
            text: "Options"
            onTriggered: options_dialog.open()
        }

        MenuSeparator { }

        Action {
            text: qsTr('Quit')
            onTriggered: close_application()
        }
    }

    Menu {
        title: qsTr('Help')

        Action {
            text: qsTr('Documentation')
            onTriggered: Qt.openUrlExternally(application.application_url)
        }

        Action {
            text: qsTr('About')
            onTriggered: about_dialog.open()
        }
    }
}

/***************************************************************************************************
 *
 * ImageBrowser — ...
 * Copyright (C) 2024 Fabrice SALVAIRE
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 **************************************************************************************************/

import QtQml.Models 2.2
import QtQuick 2.11
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11

import ImageBrowser 1.0
import Widgets 1.0 as Widgets

Widgets.CentredDialog {
    id: dialog
    implicitWidth: 800
    implicitHeight: 400

    standardButtons: Dialog.Ok | Dialog.Cancel

    // onAccepted:
    // onRejected:

    /******************************************************/

    header: TabBar {
        id: tab_bar

        TabButton {
            text: qsTr("General")
        }

        TabButton {
            text: qsTr("Shortcuts")
        }
    }

    StackLayout {
        anchors.fill: parent
        currentIndex: tab_bar.currentIndex

        Item {
            id: general_tab

            ScrollView {
                anchors.fill: parent
                clip: true
                ScrollBar.horizontal.policy: ScrollBar.AsNeeded
                ScrollBar.vertical.policy: ScrollBar.AsNeeded

                GridLayout {
                    width: general_tab.width
                    columns: 2
                    columnSpacing: 10

                    Label {
                        text: qsTr('External Program to Open Page')
                    }
                    Widgets.FileField {
                        // id:
                        Layout.fillWidth: true
                        path: application_settings.external_program
                        onPathChanged: application_settings.external_program = path
                   }

                    Label {
                        text: qsTr('Filter Script')
                    }
                    Widgets.TextField {
                        // id:
                        Layout.fillWidth: true
                        // onEditingFinished:
                    }
                }
            }
        }

        Item {
            id: shortcut_list_view_container

            ListView {
                id: shortcut_list_view
                anchors.fill: parent
                clip: true

                //! model: application_settings.shortcuts

                delegate: Widgets.ShortcutRow {
                    width: parent.width
                    shortcut: modelData
                }
            }
        }
    }
}

/***************************************************************************************************
 *
 * ImageBrowser — ...
 * Copyright (C) 2024 Fabrice SALVAIRE
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 **************************************************************************************************/

import QtQuick 2.11
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11

import Widgets 1.0 as Widgets
import Constants 1.0

Item {

    /******************************************************
     *
     * API
     *
     */

    property alias html_text: viewer.text
    property alias markdown_text: editor.text

    signal markdown_text_edited() // Fixme: onMarkdown_textChanged ???

    /******************************************************/

    id: root

    /******************************************************/

    Rectangle {
        anchors.top: root.top
        anchors.left: root.left
        height: root.height
        width: root.width - edit_button.width
        // Fixme:
        border.color: editor_container.visible ? Style.color.danger : '#ababac'

        ScrollView {
            id: viewer_container
            anchors.fill: parent

            TextArea {
                id: viewer
                wrapMode: TextEdit.Wrap
                textFormat: TextEdit.RichText
                readOnly: true
		selectByMouse: true

                // background: Rectangle {
                // }
            }

            ScrollBar.vertical.policy: ScrollBar.AlwaysOn
        }

        ScrollView {
            id: editor_container
            anchors.fill: parent
            visible: false

            TextArea {
                id: editor
                wrapMode: TextEdit.Wrap
                textFormat: TextEdit.PlainText
		selectByMouse: true

                // background: Rectangle {
                // }

                Keys.onEscapePressed: {
                    focus = false
                    event.accepted = true
                }

                onEditingFinished: {
                    markdown_text_edited()
                    // swap
                    editor_container.visible = false
                    viewer_container.visible = true
                }
            }

            ScrollBar.vertical.policy: ScrollBar.AlwaysOn
        }
    }

    Widgets.WarnedToolButton {
        id: edit_button
        anchors.top: root.top
        anchors.right: root.right

        icon.name: 'edit-black'
        tip: qsTr('Edit Markdown')
        icon.color: warned ? Style.color.danger : 'black'

        warned: editor.focus

        // When a user click on button while the editor has focus, signal order is
        //   1) editor.onEditingFinished !!!
        //   2) button.onFocuschanged
        //   3) editor.onFocuschanged
        //   4) button.onPressed
        //   5) button.onClicked

        onClicked: {
            // swap and set focus
            viewer_container.visible = false
            editor_container.visible = true
            editor.focus = true
        }
    }
}

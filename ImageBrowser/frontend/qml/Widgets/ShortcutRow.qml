/***************************************************************************************************
 *
 * ImageBrowser — ...
 * Copyright (C) 2024 Fabrice SALVAIRE
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 **************************************************************************************************/

// Forked from https://github.com/mitchcurtis/slate/blob/master/app/qml/ui/ShortcutRow.qml
// See KeySequenceEditor.py for item implementation

import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.1

import ImageBrowser 1.0

RowLayout {

    /*******************************************************
     *
     * API
     *
     */

    property var shortcut

    function reset() {
        editor.reset()
    }

    /******************************************************/

    Label {
        Layout.leftMargin: 10
        Layout.fillWidth: true
        text: shortcut.display_name
    }

    KeySequenceEditor {
        id: editor
        Layout.minimumWidth: 200
        implicitHeight: edit_button.implicitHeight

        // enabled: shortcut_name.length > 0
        default_sequence: shortcut.default_sequence

        // Fixme: name ...
        onNew_sequenceChanged: {
            console.info('New sequence', editor.new_sequence)
            shortcut.sequence = editor.new_sequence
        }

        // The fix for QTBUG-57098 probably should have been implemented in C++ as well.
        // I've tried implementing it in C++ with event() and converting the event
        // to a QKeyEvent when the type is ShortcutOverride, but it didn't work.
        Keys.onShortcutOverride: event.accepted = (event.key === Qt.Key_Escape)

        ItemDelegate {
            id: edit_button
            width: parent.width
            implicitWidth: 200
            text: editor.display_sequence
            font.bold: editor.is_customised

            onClicked: editor.forceActiveFocus()

            // Animation to blink the sequence while editing
            SequentialAnimation {
                id: flash_animation
                running: editor.activeFocus

                loops: Animation.Infinite
                alwaysRunToEnd: true

                NumberAnimation {
                    target: edit_button.contentItem
                    property: 'opacity'
                    from: 1
                    to: 0.5
                    duration: 300
                }
                NumberAnimation {
                    target: edit_button.contentItem
                    property: 'opacity'
                    from: 0.5
                    to: 1
                    duration: 300
                }
            }
        }
    }
}

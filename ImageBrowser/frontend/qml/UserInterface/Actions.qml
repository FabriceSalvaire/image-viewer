/***************************************************************************************************
 *
 * ImageBrowser — ...
 * Copyright (C) 2024 Fabrice SALVAIRE
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 **************************************************************************************************/

// pragma Singleton
// Composite Singleton Type Actions is not creatable.

import QtQuick
import QtQuick.Controls

import ImageBrowser 1.0

// Fixme: where to place Action ?

// Fixme: Type Ui.Actions unavailable
// QtObject {
// but Item is a basic visual QML type
Item {
    id: root

    /*******************************************************
     *
     * API
     *
     */

    property var image_viewer
    // application_window.load_collection

    /******************************************************/

    // Fixme: export ids
    property alias reload_action: reload_action
    property alias sort_action_group: sort_action_group

    property alias fit_to_screen_action: fit_to_screen_action
    property alias flip_action: flip_action
    property alias next_image_action: next_image_action
    property alias prev_image_action: prev_image_action
    property alias zoom_full_action: zoom_full_action
    property alias open_image_in_external_program_action: open_image_in_external_program_action

    /******************************************************
     *
     * Image Collection
     *
     */

    Action {
        id: reload_action
        icon.name: 'refresh-black'
        // shortcut: ''
        // Fixme:
        //   onTriggered: load_collection(application.collection.path)
    }

    ActionGroup {
        id: sort_action_group

        Action {
            id: sort_by_index
            checked: true
            checkable: true
            text: qsTr("Index")
            onTriggered: application.collection.sort('index')
        }

        Action {
            id: sort_by_name
            checked: false
            checkable: true
            text: qsTr("Name")
            onTriggered: application.collection.sort('name')
        }

        Action {
            id: sort_by_modified_date
            checked: false
            checkable: true
            text: qsTr("Modified date")
            onTriggered: application.collection.sort('mtime')
        }

        Action {
            id: sort_by_size
            checked: false
            checkable: true
            text: qsTr("Size")
        }
    }

    /******************************************************
     *
     * Image Viewer
     *
     */

    Action {
        id: prev_image_action
        icon.name: 'arrow-back-black'
        shortcut: application_settings.shortcut('previous_image').sequence
        onTriggered: image_viewer.prev_image()
    }

    Action {
        id: next_image_action
        icon.name: 'arrow-forward-black'
        shortcut: application_settings.shortcut('next_image').sequence
        onTriggered: image_viewer.next_image()
    }

    Action {
        id: flip_action
        icon.name: 'swap-vert-black'
        shortcut: application_settings.shortcut('flip_image').sequence
        onTriggered: image_viewer.flip()
    }

    Action {
        id: fit_to_screen_action
        icon.name: 'settings-overscan-black'
        shortcut: application_settings.shortcut('fit_to_screen').sequence
        onTriggered: image_viewer.fit_to_screen()
    }

    Action {
        id: zoom_full_action // Fixme: name
        icon.name: 'zoom-fit-width'
        shortcut: application_settings.shortcut('full_zoom').sequence
        onTriggered: image_viewer.zoom_full()
    }

    Action {
        id: open_image_in_external_program_action
        icon.name: 'open-in-new-black'
        // shortcut: application_settings.shortcut('open_image_in_external_program').sequence
        onTriggered: image_viewer.open_in_external_program()
    }
}

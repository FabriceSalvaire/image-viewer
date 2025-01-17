/***************************************************************************************************
 *
 * ImageBrowser — ...
 * Copyright (C) 2024 Fabrice SALVAIRE
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 **************************************************************************************************/

import QtQuick 2.11
import QtQuick.Controls 2.4

import ImageBrowser 1.0

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

    property alias fit_to_screen_action: fit_to_screen_action
    property alias flip_action: flip_action
    property alias next_image_action: next_image_action
    property alias prev_image_action: prev_image_action
    property alias reload_action: reload_action
    property alias zoom_full_action:zoom_full_action
    property alias open_image_in_external_program_action:open_image_in_external_program_action

    /******************************************************/

    Action {
        id: reload_action
        icon.name: 'refresh-black'
        // shortcut: ''
        onTriggered: load_collection(application.collection.path)
    }

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

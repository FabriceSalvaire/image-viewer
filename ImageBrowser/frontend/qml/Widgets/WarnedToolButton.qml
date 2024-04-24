/***************************************************************************************************
 *
 * ImageBrowser — ...
 * Copyright (C) 2024 Fabrice SALVAIRE
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 **************************************************************************************************/

import QtQuick 2.11
import QtQuick.Controls 2.4

import '.' 1.0 as Widgets

Widgets.ToolButtonTip {

    /*******************************************************
     *
     * API
     *
     */

    property bool warned: false

    /******************************************************/

    id: button

    SequentialAnimation {
        id: flash_animation
        running: warned

        loops: Animation.Infinite
        alwaysRunToEnd: true

        NumberAnimation {
            target: button
            property: 'opacity'
            from: 1
            to: 0.5
            duration: 300
        }
        NumberAnimation {
            target: button
            property: 'opacity'
            from: 0.5
            to: 1
            duration: 300
        }
    }
}

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

import ImageBrowser 1.0
import Widgets 1.0 as Widgets
import '.' 1.0 as Ui

Page {

    /*******************************************************
     *
     * API
     *
     */

    property alias image_viewer: image_viewer

    function toggle_grid() {
        grid.visible = !grid.visible
    }

    /******************************************************/

    id: root

    Component.onCompleted: {
    }

    /******************************************************/

    RowLayout {
        anchors.fill: parent

        Ui.ImageViewer {
            id: image_viewer
            Layout.fillHeight: true
            Layout.fillWidth: true

            Widgets.Grid {
                id: grid
                anchors.fill: parent
                visible: false
            }
        }
    }
}

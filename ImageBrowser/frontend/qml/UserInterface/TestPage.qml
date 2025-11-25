/***************************************************************************************************
 *
 * ImageBrowser — ...
 * Copyright (C) 2024 Fabrice SALVAIRE
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 **************************************************************************************************/

import QtQuick
import QtQuick.Controls

// import Qt.labs.folderlistmodel

import ImageBrowser 1.0
import Widgets 1.0 as Widgets
import Test 1.0 as Test

import '.' 1.0 as Ui

Page {
    id: root

    /*******************************************************
     *
     * API
     *
     */

    /******************************************************/

    /*
    Row {
        Test.FolderModelView {
            width: 200
            height: 400
        }

        Widgets.FileSystemView {
            width: 200
            height: 600

            file_system_model: application.file_system_model
        }
        }
    */

    /*
    Widgets.PathNavigator {
        width: 600
        // height: 
        }
    */

    Rectangle {
        anchors.fill: parent

        Rectangle {
            x: 200
            y: 200
            width: 100
            height: 100
            color: "green"
            antialiasing: true

            WheelHandler {
                property: "rotation"
                margin: 10
                onWheel: (event) => console.info(
                    "rotation", event.angleDelta.y,
                    "scaled", rotation, "@", point.position,
                    "=>", parent.rotation)
            }
        }
    }
}

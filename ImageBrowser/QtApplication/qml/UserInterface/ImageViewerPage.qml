/***************************************************************************************************
 *
 *  ImageBrowser - ...
 *  Copyright (C) 2024 Fabrice Salvaire
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as
 *  published by the Free Software Foundation, either version 3 of the
 *  License, or (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 *
 ***************************************************************************************************/

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

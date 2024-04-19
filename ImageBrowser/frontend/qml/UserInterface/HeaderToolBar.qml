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
import UserInterface 1.0 as Ui

ToolBar {
    id: root

    /*******************************************************
     *
     * API
     *
     */

    property var actions
    property var image_viewer_page
    property var stack_layout

    /******************************************************/

    RowLayout {
        anchors.fill: parent
        spacing: 10

        RowLayout {
            Widgets.ToolButtonTip {
                action: actions.reload_action
                tip: qsTr('Reload collection')
            }

            Widgets.ToolButtonTip {
                icon.name: 'view-comfy-black'
                tip: qsTr('Show page thumbnails')
                onClicked: stack_layout.set_thumbnail_page()
            }

            Widgets.ToolButtonTip {
                // icon.name: 'image-black'
                icon.name: 'pageview-black'
                tip: qsTr('Show page viewer')
                onClicked: stack_layout.set_viewer_page()
            }

        }

        Ui.ImageViewerToolBar {
            visible: image_viewer_page.visible

            actions: root.actions
            image_viewer: root.image_viewer_page.image_viewer
            image_viewer_page: root.image_viewer_page
        }

        Item {
            Layout.fillWidth: true
        }
    }
}

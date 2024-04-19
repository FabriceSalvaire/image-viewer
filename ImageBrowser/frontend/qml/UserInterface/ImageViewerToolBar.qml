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

RowLayout {
    id: root

    /*******************************************************
     *
     * API
     *
     */

    property var actions
    property var image_viewer
    property var image_viewer_page

    /******************************************************/

    property var collection: application.collection

    /******************************************************/

    Widgets.ToolButtonTip {
        icon.name: 'zoom-out-black'
        onClicked: image_viewer.zoom_out()
    }

    Widgets.ToolButtonTip {
        action: actions.fit_to_screen_action
    }

    Widgets.ToolButtonTip {
        action: actions.zoom_full_action
    }

    Widgets.ToolButtonTip {
        icon.name: 'zoom-in-black'
        onClicked: image_viewer.zoom_in()
    }

    Widgets.ToolButtonTip {
        icon.name: 'wrap-text-black'
        tip: qsTr('Continuous Mode')
        checkable: true
        onClicked: image_viewer.toggle_continuous_mode()
    }

    Widgets.ToolButtonTip {
        icon.name: 'first-page-black'
        onClicked: image_viewer.first_image()
    }

    Widgets.ToolButtonTip {
        action: actions.prev_image_action
    }

    Widgets.ToolButtonTip {
        // Fixme: it hangs in comparison to spinbox that looks fast
        action: actions.next_image_action
    }

    Widgets.ToolButtonTip {
        icon.name: 'last-page-black'
        onClicked: image_viewer.last_image()
    }

    SpinBox {
        id: image_index
        editable: true
        from: 0
        to: collection.number_of_images -1
        value: image_viewer.image ? image_viewer.image.index : 0

        onValueModified: image_viewer.to_image(value)
    }

    Label {
        text: '/' + collection.number_of_images
    }

    /* Widgets.ToolButtonTip { */
    /*     action: actions.flip_action */
    /*     tip: qsTr('Flip image') */
    /* } */

    Widgets.ToolButtonTip {
        action: actions.open_image_in_external_program_action
        // tip: qsTr('Open in ...')
    }
}

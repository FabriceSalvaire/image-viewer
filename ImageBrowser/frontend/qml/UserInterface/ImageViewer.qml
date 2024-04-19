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

import ImageBrowser 1.0
import Widgets 1.0 as Widgets

Widgets.ImageViewer {

    /*******************************************************
     *
     * API
     *
     */

    property var image

    property bool continuous_mode: false

    signal image_changed() // int index
    signal dirty_image(var image) // orientation changed

    function toggle_continuous_mode() {
        continuous_mode = !continuous_mode
    }

    function first_image() {
        image = collection.first_image
        image_changed()
    }

    function last_image() {
        image = collection.last_image
        image_changed()
    }

    function to_image(index) {
         if (collection.is_valid_index(index)) {
             image = collection.image(index)
             image_changed()
         }
    }

    function prev_image() {
        to_image(image.index -1)
    }

    function next_image() {
        to_image(image.index +1)
    }

    /* function flip() { */
    /*     image.flip_image() */
    /* } */

    function open_in_external_program() {
        image.open_in_external_program(application_settings.external_program)
    }

    /******************************************************/

    id: image_viewer

    property var collection: application.collection

    image_source: image ? image.path : ''
    // image_rotation: image ? image.orientation : 0

    Component.onCompleted: {
        collection.new_image.connect(last_image)
    }

    onMovementEnded: {
        // Fixme: this simple implementation has issues
        //   It require to start a flick event (a wheel event is not enought)
        //     Need a way to receive a wheel event
        //   It show glitches when the image change
        //     Disable the animation
        if (continuous_mode) {
            if (image_viewer.atYBeginning) {
                prev_image()
                image_viewer.contentY = image_viewer.contentHeight
            }
            else if (image_viewer.atYEnd) {
                next_image()
                image_viewer.contentY = 0
            }
        }
    }
}

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
import '.' 1.0 as Ui

Page {
    id: root

    /*******************************************************
     *
     * API
     *
     */

    property var image_viewer
    // property var stack_layout

    /******************************************************/

    // FocusScope {
    // FocusScope needs to bind to visual properties of the Rectangle
    // property alias color: thumbnail_container.color
    // anchors.fill: parent
    // x: thumbnail_viewer.x
    // y: thumbnail_viewer.y
    // width: thumbnail_viewer.width
    // height: thumbnail_viewer.height

    /*
    Component.onCompleted: {
        var collection = application.collection
        collection.number_of_images_changed.connect(update_text)
        update_text()
    }
    */

    Item {
        anchors.fill: parent

        Ui.ThumbnailViewer {
            id: thumbnail_viewer
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.bottom: info_bar.top
            width: parent.width
            // focus: true

            thumbnail_model: application.collection //.images

            // signal from UserInterface/ThumbnailViewer.qml
            onShow_image: {
                image_viewer.to_image(index)
                stack_layout.set_viewer_page()
            }
        }

        Rectangle {
            id: info_bar
            anchors.left: parent.left
            anchors.bottom: parent.bottom
            // anchors.top: thumbnail_viewer.bottom
            width: parent.width
            height: 60

            color: 'green'

            Text {
                id: info_bar_text
                anchors.fill: parent
                horizontalAlignment : Text.AlignHCenter
                verticalAlignment : Text.AlignVCenter
                text: ''

                function update_text() {
                    var thumbnail_model = thumbnail_viewer.thumbnail_model
                    if (thumbnail_model) {
                        var number_of_images = application.collection.number_of_images
                        var text = '%1 images'.arg(number_of_images)
                        console.info('ThumbnailPage.update_text', text)
                        info_bar_text.text = text
                    } else {
                        console.info('ThumbnailPage.update_text: undefined model')
                        info_bar_text.text = ''
                    }
                }

                Component.onCompleted: {
                    console.info('info_bar_text completed')
                    // var collection = application.collection
                    // collection.number_of_images_changed.connect(update_text)
                    // update_text()
                    application.collection_changed.connect(update_text)
                }
            }
        }
    }
    // }
}

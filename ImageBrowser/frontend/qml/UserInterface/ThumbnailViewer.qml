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

Item {
    id: thumbnail_container

    /*******************************************************
     *
     * API
     *
     */

    signal show_image(int index)

    property var thumbnail_model

    /******************************************************/

    anchors.margins: 20

    /******************************************************/

    Flickable {
        id: flickable
        anchors.fill: parent
        contentWidth: flow.width
        contentHeight: flow.height

        boundsBehavior: Flickable.StopAtBounds
        clip: true

        // ScrollView {
        Flow {
            // Fixme: QML Flow: Cannot anchor to an item that isn't a parent or sibling.
            id: flow
            width: flickable.width
            //! anchors.horizontalCenter: flickable.horizontalCenter
            // anchors.margins: 0
            spacing: 30

            Repeater {
                model: thumbnail_model

                Rectangle {
                    id: image_container

                    required property var modelData
                    property var image: modelData //.image

                    property bool selected: false
                    property int border_width: 5
                    property int image_size: image.large_thumbnail_size
                    property bool image_ready: thumbnail.status === Image.Ready

                    width:  (image_ready ? thumbnail.sourceSize.width  : image_size) + 2*border_width
                    height: (image_ready ? thumbnail.sourceSize.height : image_size) + 2*border_width
                    border.width: border_width
                    border.color: selected ? '#38b0ff' : '#00000000'
                    color: image_ready ? '#00000000' :'#aaaaaa'

                    BusyIndicator {
                        anchors.centerIn: parent
                        // running: !(image.is_empty || image_ready)
                        running: !image_ready
                    }

                    Text {
                        // visible: thumbnail.status !== Image.Ready
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.top: parent.top
                        anchors.topMargin: 20
                        font.pixelSize: image_size * .10
                        text: 'P' + image.index
                        z: 100
                    }

                    Image {
                        id: thumbnail
                        anchors.centerIn: parent
                        // visible: ! image.is_empty

                        asynchronous: true
                        // rotation: image.orientation

                        MouseArea {
                            anchors.fill: parent
                            hoverEnabled: true
                            onClicked: thumbnail_container.show_image(image.index)
                            onEntered: selected = true
                            onExited: selected = false
                        }

                        function log_thumbnail_info() {
                            console.info(source, image_size)
                        }

                        Component.onCompleted: {
                            // if (!image.is_empty)
                            source = image.large_thumbnail_path
                            log_thumbnail_info()
                        }

                        function on_thumbnail_ready() {
                            source = image.large_thumbnail_path
                            log_thumbnail_info()
                        }

                        onStatusChanged: {
                            if (thumbnail.status == Image.Error) {
                                source = ''
                                image.request_large_thumbnail()
                                image.thumbnail_ready.connect(on_thumbnail_ready)
                            }
                        }
                    }
                }
            }
        }

        // ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
        // ScrollBar.vertical.policy: ScrollBar.AlwaysOn
        ScrollIndicator.vertical: ScrollIndicator { }
        // ScrollIndicator.horizontal: ScrollIndicator { }
    }
}

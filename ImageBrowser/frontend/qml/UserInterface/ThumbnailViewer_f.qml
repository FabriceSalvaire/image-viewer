/***************************************************************************************************
 *
 * ImageBrowser — ...
 * Copyright (C) 2024 Fabrice SALVAIRE
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 **************************************************************************************************/

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

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

    Component.onCompleted: {
        // console.info("Focus", activeFocus)
        // focus = true
        console.info("Focus", activeFocus)
        console.info("StandardKey", StandardKey.MoveToNextPage)
    }

    Keys.onPressed: (event) => {
        console.info('key', event)
        // Qt.Key_PageUp
        if (event.key == Qt.Key_Enter)
            console.info('ENTER')
    }

    Shortcut {
        sequence: StandardKey.MoveToNextPage
        // sequence: Qt.Key_PageUp
        onActivated: {
            console.info('shortcut')
            scrollbar.increase()
        }
    }

    Shortcut {
        id: shortcut1
        sequence: StandardKey.MoveToPreviousPage
        // sequence: 'PgUp'
        enabled: true
        onActivated: {
            console.info('shortcut1')
            scrollbar.decrease()
            // enabled = false
            // shortcut2.enabled = true
        }
    }

    Shortcut {
        id: shortcut2
        sequence: StandardKey.MoveToPreviousPage
        // sequence: 'PgUp'
        enabled: false
        onActivated: {
            console.info('shortcut2')
            enabled = false
            shortcut1.enabled = true
        }
    }

    Flickable {
        id: flickable
        anchors.fill: parent
        contentWidth: flow.width
        contentHeight: flow.height

        flickableDirection: Flickable.VerticalFlick
        // flickDeceleration: 0.1
        // maximumFlickVelocity: 5000
        boundsBehavior: Flickable.StopAtBounds
        clip: true

        interactive: true
        /*
        MouseArea
        {
            id: mousearea
            anchors.fill: parent
            preventStealing: true

            property real angle_accumulator: 0
            property real angle_threshold: 120
            property real angle_threshold2: 360

            onWheel: event => {
                var angle = event.angleDelta.y
                console.info('wheel', angle, angle_accumulator)
                if (Math.abs(angle) < angle_threshold) {
                    angle_accumulator += angle
                    if (angle_accumulator > angle_threshold2) {
                        angle_accumulator = 0
                        angle = 1
                    } else if (angle_accumulator < -angle_accumulator2) {
                        angle_accumulator = 0
                        angle = -1
                    } else
                        return
                }
                if (angle > 0)
                    scrollbar.decrease()
                else
                    scrollbar.increase()
            }
        }
        */

        // ScrollView {
        Flow {
            // Fixme: QML Flow: Cannot anchor to an item that isn't a parent or sibling
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
                    property var image: modelData // .image

                    property bool selected: false
                    property int border_width: 5
                    property int image_size: image.large_thumbnail_size
                    property bool image_ready: thumbnail.status === Image.Ready

                    // width:  (image_ready ? thumbnail.sourceSize.width  : image_size) + 2*border_width
                    // height: (image_ready ? thumbnail.sourceSize.height : image_size) + 2*border_width
                    width:  image_size + 2*border_width
                    height: image_size + 2*border_width
                    border.width: border_width
                    border.color: selected ? '#38b0ff' : '#00000000'
                    color: image_ready ? '#00000000' :'#aaaaaa'

                    BusyIndicator {
                        anchors.centerIn: parent
                        // running: !(image.is_empty || image_ready)
                        running: !image_ready
                    }

                    Text {
                        // Paint Pindex over image
                        // visible: thumbnail.status !== Image.Ready
                        anchors.top: parent.top
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.topMargin: 20
                        font.pixelSize: image_size * .10
                        text: 'P' + image.index
                        z: 100
                    }

                    Image {
                        // Qt try to load the image from a local path
                        // if it fails
                        //   because the thumbnail doesn't exists
                        // then we request to generate it
                        // we use the hack to clear and reset source
                        //   to trigger a new loading
                        // QQuickImageProvider
                        //   source: "image://myimageprovider/image.png"

                        id: thumbnail
                        anchors.centerIn: parent
                        // visible: ! image.is_empty

                        // load images on the local filesystem in a separate thread
                        asynchronous: true
                        // rotation: image.orientation

                        // Fixme: move parent ?
                        MouseArea {
                            anchors.fill: parent
                            hoverEnabled: true
                            onClicked: thumbnail_container.show_image(image.index)
                            // Fixme: to paint border
                            //   hover ?
                            onEntered: selected = true
                            onExited: selected = false
                        }

                        function log_thumbnail_info() {
                            console.info(source, image_size)
                        }

                        Component.onCompleted: {
                            // if (!image.is_empty)
                            // Set Image.source to the thumbnail path
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

        ScrollBar.vertical: ScrollBar {
            id: scrollbar
            width: 16
            stepSize: .01
        }
        // ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
        // ScrollBar.vertical.policy: ScrollBar.AlwaysOn
        // ScrollIndicator.vertical: ScrollIndicator { }
        // ScrollIndicator.horizontal: ScrollIndicator { }
    }
}

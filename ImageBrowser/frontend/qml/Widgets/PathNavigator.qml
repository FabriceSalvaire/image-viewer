/***************************************************************************************************
 *
 * ImageBrowser — ...
 * Copyright (C) 2024 Fabrice SALVAIRE
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 **************************************************************************************************/

import QtQuick
import QtQuick.Controls
// import QtQuick.Controls.Styles
import QtQuick.Layouts
// import Qt.labs.platform

import Constants 1.0

Rectangle {
    id: path_navigator

    anchors.fill: parent

    // color: application_style.window_color

    ListModel {
        id: path_model
    }

    ListModel {
        id: directory_model
    }

    function fill_path_model() {
        for (var i = 0; i < 4; i++)
            path_model.insert(i, {'name': 'dir' + i})
    }

    function fill_directory_model(index: int) {
        for (var i = 0; i < 4; i++)
            directory_model.insert(i, {'name': path_model.get(index).name + '/dir' + i})
    }

    Component.onCompleted: {
        console.info('PathNavigator')
        fill_path_model()
    }

    Component {
        id: partDelegate1
        RowLayout {
            // Row don't center vertically
            // spacing: 2

            Text {
                text: name
            }

            /*
            Text {
                text: '>'
            }
            */

            /* Image { */
            /*     source: '../../rcc/icons/material/36x36/chevron-right-black.png' */
            /* } */

            // AbstractButton : no display
            Button {
                // text: '>'
                // for qml utility
                icon.source: '/home/fabrice/home/developpement/python/image-viewer/rcc/icons/material/36x36/chevron-right-black.png'
                // icon.name: 'chevron-right-black'
                // icon.name: 'arrow-forward-black' // works ???
                background: Rectangle {
                    implicitWidth: 36
                    implicitHeight: 36
                    // color: button.down ? "#d6d6d6" : "#f6f6f6"
                }
            }

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    console.info('Clicked on directory', model.index)
                }
            }
        }
    }

    Component {
        id: partDelegate2
        Rectangle {
            width:  childrenRect.width
            height: childrenRect.height

            border.color: 'black'
            border.width: 1
            radius: 4

            MouseArea {
                width:  childrenRect.width
                height: childrenRect.height
                onClicked: {
                    console.info('Clicked on directory', model.index)
                }

                RowLayout {
                    Text {
                        Layout.leftMargin: 5
                        text: name
                    }
                    Button {
                        Layout.margins: 5
                        // for qml utility
                        icon.source: '/home/fabrice/home/developpement/python/image-viewer/rcc/icons/material/36x36/chevron-right-black.png'
                        background: Rectangle {
                            implicitWidth: 36
                            implicitHeight: 36
                            // color: button.down ? "#d6d6d6" : "#f6f6f6"
                        }
                    }
                }
            }
        }
    }

    Component {
        id: partDelegate
        Rectangle {
            id: partRectangle
            width:  childrenRect.width
            height: childrenRect.height

            border.color: 'black'
            border.width: partMouseArea.containsMouse ? 1 : 0
            radius: 4
            // color: partMouseArea.pressed ? '#dddddd' : 'white'

            property int chevron_width: 36 

            function on_chevron(mouse: MouseEvent) : bool {
                var _ = mouse.x > (partRectangle.width - chevron_width) ? true : false
                // console.info(mouse.x, _)
                return _
            }

            function on_chevron2() : bool {
                // if partMouseArea.containsMouse
                var _ = partMouseArea.mouseX > (partRectangle.width - chevron_width) ? true : false
                return _
            }

            MouseArea {
                id: partMouseArea
                anchors.fill: parent
                hoverEnabled: true
                onClicked: (mouse) => {
                    var _ = on_chevron(mouse)
                    console.info('Clicked on directory', _, model.index)
                    if (_) {
                        fill_directory_model(model.index)
                        menu.popup()
                    } else
                        console.info('on part')
                }
            }

            Row {
                leftPadding: 5
                rightPadding: 5
                topPadding: 2
                bottomPadding: 2

                spacing: 0

                Text {
                    id: partText
                    anchors.verticalCenter: parent.verticalCenter
                    text: name
                }

                Image {
                    id: chevron
                    width: chevron_width
                    source: '../../rcc/icons/material/36x36/chevron-right-black.png'
                    mirror: partMouseArea.containsMouse && on_chevron2() ? true : false
                }

                /*
                Button {
                    id: chevron
                    // icon.source: '/home/fabrice/home/developpement/python/image-viewer/rcc/icons/material/36x36/chevron-right-black.png'
                    icon.source: '../../rcc/icons/material/36x36/chevron-right-black.png'
                    background: Rectangle {
                        // implicitWidth: 36
                        // implicitHeight: 36
                        color: chevron.down ? '#dddddd' : 'white'
                    }
                    }
                */
            }
        }
    }

    ListView {
        anchors.fill: parent
        anchors.margins: Style.spacing.base
        orientation: ListView.Horizontal
        spacing: 3 // Style.spacing.base_horizontal

        model: path_model
        delegate: partDelegate
    }

    Menu {
        id: menu

        Instantiator {
            model: directory_model
            onObjectAdded: (index, object) => menu.insertItem(index, object)
            onObjectRemoved: (index, object) => menu.removeItem(object)
            delegate: MenuItem {
                text: name
                onTriggered: console.info('clicked on directory', name)
            }
        }
    }
}

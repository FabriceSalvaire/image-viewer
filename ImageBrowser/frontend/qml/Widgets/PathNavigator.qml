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

    property int icon_size: 24

    property bool edit_mode: false

    ListModel {
        id: path_model
    }

    ListModel {
        id: directory_model
    }

    ListModel {
        id: completion_model

        ListElement {
            path: '/foo/bar/ba'
        }

        ListElement {
            path: '/bar/foo/bb'
        }
    }

    ListModel {
        id: history_model

        ListElement {
            path: '/foo/bar'
        }

        ListElement {
            path: '/bar/foo'
        }
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
        id: part_delegate
        Rectangle {
            id: part_rectangle
            width:  childrenRect.width
            height: childrenRect.height
            anchors.verticalCenter: parent.verticalCenter // !

            border.color: 'black'
            border.width: part_mouse_area.containsMouse ? 1 : 0
            radius: 4
            // color: part_mouse_area.pressed ? '#dddddd' : 'white'

            Component.onCompleted: {
                console.info(
                    'part_rectangle',
                    part_rectangle.height,
                    part_row.height,
                    part_text.height, part_text.contentHeight,
                    chevron_icon.height
                )
            }

            MouseArea {
                id: part_mouse_area
                anchors.fill: parent
                hoverEnabled: true
                onClicked: (mouse) => {
                    var _ = is_on_chevron(mouse)
                    console.info('Clicked on directory', _, model.index)
                    if (_) {
                        fill_directory_model(model.index)
                        subdirectory_menu.popup()
                    } else
                        console.info('  on part')
                }

                function is_on_chevron(mouse: MouseEvent) : bool {
                    var _ = mouse.x < icon_size
                    // console.info(mouse.x, _)
                    return _
                }
            }

            Row {
                id: part_row
                // anchors.verticalCenter: parent.verticalCenter
                leftPadding: 0
                rightPadding: 2
                topPadding: 2
                bottomPadding: 2

                spacing: 0

                Image {
                    id: chevron_icon
                    height: icon_size
                    fillMode: Image.PreserveAspectFit
                    verticalAlignment: Image.AlignVCenter
                    source: '../../rcc/icons/material/36x36/chevron-right-black.png'
                    mirror: part_mouse_area.containsMouse && is_on_chevron2()

                    function is_on_chevron2() : bool {
                        // if part_mouse_area.containsMouse
                        var _ = part_mouse_area.mouseX < icon_size
                        return _
                    }
                }

                Text {
                    id: part_text
                    // anchors.verticalCenter: parent.verticalCenter
                    text: name
                    font.pixelSize: 16
                    // font.family: ''
                }
            }
        }
    }

    Rectangle {
        id: root_element
        width: 500
        height: icon_size + 2*10

        border.color: 'black'
        border.width: 1
        radius: 4

        Rectangle {
            id: part_root_element
            anchors.fill: parent
            visible: !edit_mode

            anchors.margins: 2

            Component.onCompleted: {
                console.info(
                    'part_root_element',
                    part_root_element.height,
                    list_view.height,
                    edit_icon.height
                )
            }

            ListView {
                id: list_view
                anchors.fill: parent
                // height: icon_size + 2*5
                // width: parent.width
                // anchors.left: parent.left
                // anchors.verticalCenter: parent.verticalCenter
                anchors.leftMargin: 5 // Style.spacing.base
                orientation: ListView.Horizontal
                spacing: 3 // Style.spacing.base_horizontal

                model: path_model
                delegate: part_delegate
            }

            Image {
                id: edit_icon
                anchors.rightMargin: 5
                anchors.verticalCenter: parent.verticalCenter
                anchors.right: parent.right
                height: icon_size
                fillMode: Image.PreserveAspectFit
                verticalAlignment: Image.AlignVCenter
                source: '../../rcc/icons/material/36x36/edit-black.png'
                visible: mouse_area.containsMouse

                /*
                  && is_on_edit_area()
                  function is_on_edit_area() : bool {
                  return mouse_area.mouseX > list_view.contentWidth
                  }
                */
            }

            Rectangle {
                anchors.verticalCenter: parent.verticalCenter
                anchors.right: parent.right
                color: 'blue'
                opacity: .1
                width: parent.width - list_view.contentWidth - 5
                height: list_view.height

                MouseArea {
                    id: mouse_area
                    anchors.fill: parent
                    hoverEnabled: true
                    /*
                      onEntered: {
                      console.log(
                      'entered',
                      list_view.contentWidth,
                      mouse_area.mouseX,
                      )
                      }
                    */
                    onClicked: (mouse) => {
                        console.log('clicked edit area')
                        edit_mode = true
                    }
                }
            }
        }

        Rectangle {
            id: edit_root_element
            anchors.fill: parent
            anchors.margins: 2
            visible: edit_mode

            RowLayout {
                anchors.fill: parent

                Text {
                    id: completion
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    // Layout.alignment: Qt.AlignVCenter
                    verticalAlignment: TextInput.AlignVCenter
                    Layout.leftMargin: 10

                    text: ''
                    color: '#888888'

                    TextInput {
                        id: text_input
                        anchors.verticalCenter: parent.verticalCenter
                        focus: true
                        text: '/foo/bar/'
                        onTextEdited: {
                            console.log('text', text)
                            completion.text = text + '...'
                            var pos = Qt.point(text_input.x, text_input.y + text_input.height + 5)
                            history_menu.popup(pos)
                            text_input.forceActiveFocus()
                        }
                        Keys.onTabPressed: (event) => {
                            // if (event.key == Qt.Key_Tab) {
                            text = text + 'completed'
                            event.accepted = true
                            // Fixme: update completion model
                        }
                    }
                }
                Button {
                    flat: true
                    text: 'C'
                    Layout.preferredWidth: icon_size
                    onClicked: {
                        text_input.clear()
                        text_input.forceActiveFocus()
                    }
                }
                Button {
                    flat: true
                    text: 'H'
                    Layout.preferredWidth: icon_size
                    onClicked: {
                        console.log('H')
                        history_menu.popup()
                    }
                }
                Button {
                    flat: true
                    text: 'V'
                    Layout.preferredWidth: icon_size
                    onClicked: {
                        console.log('V', text_input.text)
                        edit_mode = false
                    }
                }
            }
        }
    }

    Menu {
        id: subdirectory_menu

        Instantiator {
            model: directory_model
            onObjectAdded: (index, object) => subdirectory_menu.insertItem(index, object)
            onObjectRemoved: (index, object) => subdirectory_menu.removeItem(object)
            delegate: MenuItem {
                text: name
                onTriggered: console.info('clicked on directory', name)
            }
        }
    }

    Menu {
        id: completion_menu

        Instantiator {
            model: completion_model
            onObjectAdded: (index, object) => completion_menu.insertItem(index, object)
            onObjectRemoved: (index, object) => completion_menu.removeItem(object)
            delegate: MenuItem {
                text: path
                onTriggered: console.info('clicked on path', path)
                // Complete: set path navigator to
            }
        }
    }

    Menu {
        id: history_menu

        Instantiator {
            model: history_model
            onObjectAdded: (index, object) => history_menu.insertItem(index, object)
            onObjectRemoved: (index, object) => history_menu.removeItem(object)
            delegate: MenuItem {
                text: path
                onTriggered: console.info('clicked on path', path)
                // Complete: set path navigator to
            }
        }
    }
}

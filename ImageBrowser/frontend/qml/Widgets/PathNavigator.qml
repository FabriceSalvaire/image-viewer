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
    property int part_index: -1
    property string default_completion: ''

    ListModel {
        id: path_model
    }

    ListModel {
        id: directory_model
    }

    ListModel {
        id: completion_model

        /*
        ListElement {
            path: '/foo/bar/ba'
        }

        ListElement {
            path: '/bar/foo/bb'
            }
        */
    }

    ListModel {
        id: history_model

        ListElement {
            path: '/h1/foo/bar'
        }

        ListElement {
            path: '/h2/bar/foo'
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

    function fill_completion_model(completions: var) {
        completion_model.clear()
        // index 0 is default
        for (var i = 1; i < completions.length; i++)
            completion_model.insert(i-1, {'name': completions[i]})
    }

    function set_edit_mode() {
        default_completion = ''
        completion.text = ''
        text_input.text = application.path_navigator.path_str
        edit_mode = true
        text_input.forceActiveFocus()
    }

    function unset_edit_mode() {
        part_index = -1
        default_completion = ''
        edit_mode = false
    }

    Component.onCompleted: {
        console.info('PathNavigator', application.path_navigator.path_parts)
        // fill_path_model()
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

            /*
            Component.onCompleted: {
                console.info(
                    'part_rectangle',
                    part_rectangle.height,
                    part_row.height,
                    part_text.height, part_text.contentHeight,
                    chevron_icon.height
                )
            }
            */

            MouseArea {
                id: part_mouse_area
                anchors.fill: parent
                hoverEnabled: true
                onClicked: (mouse) => {
                    var _ = is_on_chevron(mouse)
                    console.info('Clicked on directory', _, model.index)
                    part_index = model.index
                    if (_) {
                        // fill_directory_model(model.index)
                        // application.path_navigator.list_parent(model.index)
                        application.path_navigator.set_parent_subdirectory(part_index)
                        subdirectory_menu.popup()
                    } else {
                        console.info('  on part', model.index)
                        application.path_navigator.cd_parent(part_index)
                    }
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
                    // source: '../../rcc/icons/material/36x36/chevron-right-black.png'
                    source: 'qrc:/icons/material/36x36/chevron-right-black.png'
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
                    // text: name
                    text: modelData
                    font.pixelSize: 16
                    // font.family: ''
                }
            }
        }
    }

    Rectangle {
        id: root_element
        width: 800
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

                // model: path_model
                model: application.path_navigator.path_parts
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
                // source: '../../rcc/icons/material/36x36/edit-black.png'
                source: 'qrc:/icons/material/36x36/edit-black.png'
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
                      console.info(
                      'entered',
                      list_view.contentWidth,
                      mouse_area.mouseX,
                      )
                      }
                    */
                    onClicked: (mouse) => {
                        // Fixme: don't log
                        console.info('clicked edit area')
                        set_edit_mode()
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
                        text: ''
                        // onTextChanged: {
                        onTextEdited: {
                            completion_menu.close()
                            // console.info('complete text', text)
                            var completions = application.path_navigator.complete(text)
                            console.info('complete text', text, completions)
                            if (completions.length) {
                                default_completion = completions[0]
                                completion.text = default_completion
                                fill_completion_model(completions)
                                var pos = Qt.point(text_input.x, text_input.y + text_input.height + 5)
                                completion_menu.popup(pos)
                            }
                            text_input.forceActiveFocus()
                        }
                        Keys.onTabPressed: (event) => {
                            // if (event.key == Qt.Key_Tab) {
                            if (default_completion)
                                text = default_completion
                            event.accepted = true
                            // Fixme: update completion model
                        }
                    }
                }

                // Dolphin W70 H16
                ToolButton {
                    flat: true
                    // text: 'C'
                    icon.name: 'backspace-black'
                    icon.height: icon_size
                    icon.width: icon_size
                    // Layout.preferredWidth: icon_size
                    onClicked: {
                        console.info('clear')
                        default_completion = ''
                        completion.text = ''
                        text_input.clear()
                        text_input.forceActiveFocus()
                    }
                }
                ToolButton {
                    flat: true
                    // text: 'H'
                    icon.name: 'keyboard-arrow-down-black'
                    icon.height: icon_size
                    icon.width: icon_size
                    // Layout.preferredWidth: icon_size
                    onClicked: {
                        console.info('history')
                        history_menu.popup()
                    }
                }
                ToolButton {
                    flat: true
                    // text: 'V'
                    icon.name: 'check-black'
                    icon.height: icon_size
                    icon.width: icon_size
                    // Layout.preferredWidth: icon_size
                    onClicked: {
                        console.info('validate', text_input.text)
                        application.path_navigator.path_str = text_input.text
                        unset_edit_mode()
                    }
                }
            }
        }
    }

    Menu {
        id: subdirectory_menu

        Instantiator {
            // model: directory_model
            model: application.path_navigator.parent_subdirectories
            onObjectAdded: (index, object) => subdirectory_menu.insertItem(index, object)
            onObjectRemoved: (index, object) => subdirectory_menu.removeItem(object)
            delegate: MenuItem {
                // text: name
                text: modelData
                onTriggered: {
                    var directory = modelData
                    console.info('clicked on directory', part_index, directory)
                    application.path_navigator.cd_parent_subdirectory(part_index, directory)
                }
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
                text: name
                onTriggered: {
                    console.info('clicked on path', name)
                    // Complete: set path navigator to
                    default_completion = ''
                    completion.text = ''
                    text_input.text = application.path_navigator.complete_with(text_input.text, name)
                }
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

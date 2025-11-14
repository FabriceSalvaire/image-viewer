/***************************************************************************************************
 *
 * ImageBrowser — ...
 * Copyright (C) 2024 Fabrice SALVAIRE
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 **************************************************************************************************/

// Fixme: push crash sane, image_viewer ???

import QtQuick 2.11
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11

import ImageBrowser 1.0
import Widgets 1.0 as Widgets
import UserInterface 1.0 as Ui

ApplicationWindow {
    id: application_window

    /*******************************************************
     *
     * API
     *
     */

     property var shortcuts: null

    function close_application(close) {
        console.info('Close application', close)
        show_message(qsTr('Close ...'))
        // WARNING - ThumbnailViewer.qml None —
        //   /qml/UserInterface/ThumbnailViewer.qml:72:
        //   TypeError: Cannot read property 'large_thumbnail_size' of null
        if (!close)
            Qt.quit()
        // else
        //    close.accepted = false
    }

    function clear_message() {
        footer_tool_bar.message = ''
    }

    function show_message(message) {
        footer_tool_bar.message = message
    }

    function load_collection(path) {
        application.load_collection(path)
        stack_layout.set_thumbnail_page()
        show_message(qsTr('Loaded collection at %1'.arg(path)))
    }

    /*******************************************************
     *
     *
     */

    title: qsTr('ImageCollection Viewer') // Fixme: ???
    visible: true
    width: 1000
    height: 500

    Component.onCompleted: {
        console.info('ApplicationWindow.onCompleted')
        console.info(application.collection)
        // Fixme: Could not find receiver of the connection, using sender as receiver.
        //  Disconnect explicitly (or delete the sender) to make sure the connection is removed.
        application.show_message.connect(on_message)
        application.show_error.connect(on_error)
        application_window.showMaximized()
        image_viewer_page.image_viewer.first_image()

        // Fixme: prevent crash when opening option dialog
        //   RuntimeError: wrapped C/C++ object of type Shortcut has been deleted
        let _shortcuts = application_settings.shortcuts
        shortcuts = {} // []
        for (var shortcut in _shortcuts)
            console.info('shortcut', shortcut)
        for (var i = 0; i < _shortcuts.length; i++) {
            var shortcut = _shortcuts[i]
            console.info('shortcut', i, shortcut)
            shortcuts[shortcut.name] = shortcut
            // shortcuts.push(shortcut)
        }
    }

    function on_message(message: string) {
        error_message_dialog.open_with_message(message)
    }

    function on_error(message: string, backtrace: string) {
        var text = message + '\n' + backtrace
        error_message_dialog.open_with_message(text)
    }

    /*******************************************************
     *
     * Slots
     *
     */

    onClosing: close_application(close)

    /*******************************************************
     *
     * Dialogs
     *
     */

    Widgets.AboutDialog {
        id: about_dialog
        title: qsTr('About ImageCollection Browser')
        about_message: application.about_message // qsTr('...')
    }

    Widgets.ErrorMessageDialog {
        id: error_message_dialog
        title: qsTr('An error occurred in ImageCollection Browser')
    }

    Widgets.NativeFolderDialog {
        id: collection_folder_dialog
        onAccepted: load_collection(selected_path())
    }

    Ui.OptionsDialog {
        id: options_dialog
    }

    /*******************************************************
     *
     * Actions
     *
     */

    Ui.Actions {
        id: actions
        image_viewer: image_viewer_page.image_viewer
    }

    /*******************************************************
     *
     * Menu
     *
     */

    // Fixme: use native menu ???
    menuBar: Ui.MenuBar {
        id: menu_bar
        about_dialog: about_dialog
        collection_folder_dialog: collection_folder_dialog
        options_dialog: options_dialog
    }

    /*******************************************************
     *
     * Header
     *
     */

    header: Ui.HeaderToolBar {
        id: header_tool_bar
        actions: actions
        image_viewer_page: image_viewer_page
        stack_layout: stack_layout
    }

    /*******************************************************
     *
     * Items
     *
     */

    StackLayout {
        id: stack_layout
        anchors.fill: parent

        function set_thumbnail_page() { currentIndex = 0 }
        function set_viewer_page() { currentIndex = 1 }
        function set_test_page() { currentIndex = 2 }

        Component.onCompleted: {
            // set_thumbnail_page()
            set_test_page()
        }

        // Fixme: simplify with Page { Widget{} } ???
        Ui.ThumbnailPage {
            id: thumbnail_page
            image_viewer: image_viewer_page.image_viewer
        }

        Ui.ImageViewerPage {
            id: image_viewer_page
        }

        Ui.TestPage {
            id: test_page
        }
    }

    /*******************************************************
     *
     * Footer
     *
     */

    footer: Ui.FooterToolBar {
        id: footer_tool_bar
    }
}

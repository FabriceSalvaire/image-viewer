/***************************************************************************************************
 *
 * ImageBrowser — ...
 * Copyright (C) 2024 Fabrice SALVAIRE
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 **************************************************************************************************/

// Test FolderListModel
//   render a vertical list of Text with filename for the current working directory

import QtQuick 2.11
import QtQuick.Controls 2.4

// https://doc.qt.io/qt-6/qml-qt-labs-folderlistmodel-folderlistmodel.html
import Qt.labs.folderlistmodel 2.7

import ImageBrowser 1.0
import '.' 1.0 as Ui

ListView {
    id: root

    width: 200; height: 400

    FolderListModel {
        id: folder_model
        // folder:
        // nameFilters: ["*.qml"]
    }

    Component {
        id: file_delegate
        // Fixme: Component objects cannot declare new properties
        // required property string fileName
        Text {
            text: fileName
        }
    }

    model: folder_model
    delegate: file_delegate
}

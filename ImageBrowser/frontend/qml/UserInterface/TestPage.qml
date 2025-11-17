/***************************************************************************************************
 *
 * ImageBrowser — ...
 * Copyright (C) 2024 Fabrice SALVAIRE
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 **************************************************************************************************/

import QtQuick 2.11
import QtQuick.Controls 2.4

import Qt.labs.folderlistmodel 2.7

import ImageBrowser 1.0
import Widgets 1.0 as Widgets
import Test 1.0 as Test

import '.' 1.0 as Ui

Page {
    id: root

    /*******************************************************
     *
     * API
     *
     */

    /******************************************************/

    /*
    Row {
        Test.FolderModelView {
            width: 200
            height: 400
        }

        Widgets.FileSystemView {
            width: 200
            height: 600

            file_system_model: application.file_system_model
        }
        }
    */

    Widgets.PathNavigator {
        width: 600
        // height: 
    }
}

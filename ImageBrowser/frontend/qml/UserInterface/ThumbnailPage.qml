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

    Ui.ThumbnailViewer {
        id: thumbnail_viewer
        anchors.fill: parent

        thumbnail_model: application.collection //.images

        onShow_image: {
            image_viewer.to_image(index)
            stack_layout.set_viewer_page()
        }
    }
}

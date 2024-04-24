/***************************************************************************************************
 *
 * ImageBrowser — ...
 * Copyright (C) 2024 Fabrice SALVAIRE
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 **************************************************************************************************/

import QtQuick 2.11
import QtQuick.Controls 2.4

import Widgets 1.0 as Widgets

Widgets.CentredDialog {

    /******************************************************
     *
     * API
     *
     */

    function open_with_message(message) {
        text_area.text = message
        open()
    }

    /******************************************************/

    id: dialog
    modal: true
    standardButtons: Dialog.Ok

    TextArea {
        id: text_area
        width: 800
        anchors.margins: 20
        wrapMode: TextEdit.Wrap
        textFormat: TextEdit.RichText
    }
}

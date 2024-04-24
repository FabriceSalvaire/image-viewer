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

ToolBar {
    id: root

    /*******************************************************
     *
     * API
     *
     */

    property alias message: message_label.text

    /******************************************************/

    RowLayout {
        Label {
            id: message_label
        }
    }
}

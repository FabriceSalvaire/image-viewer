/***************************************************************************************************
 *
 * ImageBrowser — ...
 * Copyright (C) 2024 Fabrice SALVAIRE
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 **************************************************************************************************/

import QtQuick 2.11
import QtQuick.Controls 2.4
import Qt.labs.platform 1.1

FileDialog {

    /******************************************************
     *
     * API
     *
     */

    function selected_path() {
        return currentFile
    }

    /******************************************************/

    id: root
    fileMode : FileDialog.SaveFile
}

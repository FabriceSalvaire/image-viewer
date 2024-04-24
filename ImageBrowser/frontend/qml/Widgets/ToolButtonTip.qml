/***************************************************************************************************
 *
 * ImageBrowser — ...
 * Copyright (C) 2024 Fabrice SALVAIRE
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 **************************************************************************************************/

import QtQuick 2.11
import QtQuick.Controls 2.4

ToolButton {
    // property alias tip: ToolTip.text
    property string tip: ''
    property int size: 22

    icon.height: size
    icon.width: size

    hoverEnabled: tip
    ToolTip.delay: 1000
    ToolTip.timeout: 5000
    ToolTip.visible: enabled && hovered
    ToolTip.text: tip
}

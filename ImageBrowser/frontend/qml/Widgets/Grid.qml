/***************************************************************************************************
 *
 * ImageBrowser — ...
 * Copyright (C) 2024 Fabrice SALVAIRE
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 **************************************************************************************************/

import QtQuick 2.11
import QtQuick.Shapes 1.11

Item {
    id: grid

    Repeater {
        model: [.1, .25, .5, .75]

        Shape {
            anchors.fill: parent

            ShapePath {
                strokeWidth: 3
                strokeColor: '#222222'

                startX: 0
                startY: grid.height * modelData

                PathLine { x: grid.width; relativeY: 0 }
            }
        }
    }
}

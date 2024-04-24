/***************************************************************************************************
 *
 * ImageBrowser — ...
 * Copyright (C) 2017 Fabrice SALVAIRE
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 **************************************************************************************************/

// from Fusion

import QtQml 2.11
import QtQuick 2.11
import QtQuick.Templates 2.4 as T
import QtQuick.Controls 2.4
import QtQuick.Controls.impl 2.4
import QtQuick.Controls.Fusion 2.4
import QtQuick.Controls.Fusion.impl 2.4

T.Button {
    id: control

    property color color_label
    property color color_background
    property color color_background_down

    implicitWidth: Math.max(background ? background.implicitWidth : 0,
                            contentItem.implicitWidth + leftPadding + rightPadding)
    implicitHeight: Math.max(background ? background.implicitHeight : 0,
                             contentItem.implicitHeight + topPadding + bottomPadding)
    baselineOffset: contentItem.y + contentItem.baselineOffset

    padding: 4
    spacing: 6

    icon.width: 16
    icon.height: 16

    contentItem: IconLabel {
        spacing: control.spacing
        mirrored: control.mirrored
        display: control.display

        icon: control.icon
        text: control.text
        font: control.font
        // color: control.palette.buttonText
        color: control.color_label
    }

    // background: ButtonPanel {
    //     implicitWidth: 80
    //     implicitHeight: 24
    //
    //     control: control
    //     visible: !control.flat || control.down || control.checked || control.highlighted || control.visualFocus || control.hovered
    // }

    background: Rectangle {
        id: panel

        implicitWidth: 80
        implicitHeight: 24

        // property Item control
        property bool highlighted: control.highlighted

        // visible: !control.flat || control.down || control.checked
        visible: !control.flat || control.down || control.checked || control.highlighted || control.visualFocus || control.hovered

        // color: Fusion.buttonColor(control.palette, panel.highlighted, control.down || control.checked, control.hovered)
        color: control.down ? Qt.darker(control.color_background, 1.1) :
            (control.hovered ? Qt.lighter(control.color_background, 1.1): control.color_background)
        // gradient: control.down || control.checked ? null : buttonGradient

        // Gradient {
        //     id: buttonGradient
        //     GradientStop {
        //      position: 0
        //      color: Fusion.gradientStart(Fusion.buttonColor(control.palette, panel.highlighted, control.down, control.hovered))
        //     }
        //     GradientStop {
        //      position: 1
        //      color: Fusion.gradientStop(Fusion.buttonColor(control.palette, panel.highlighted, control.down, control.hovered))
        //     }
        // }

        // radius: 2
        radius: 10
        // border.color: Fusion.buttonOutline(control.palette, panel.highlighted || control.visualFocus, control.enabled)

        // Rectangle {
        //     x: 1; y: 1
        //     width: parent.width - 2
        //     height: parent.height - 2
        //     border.color: Fusion.innerContrastLine
        //     color: "transparent"
        //     radius: 2
        // }
    }
}

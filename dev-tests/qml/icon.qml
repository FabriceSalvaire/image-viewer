import QtQuick
import QtQuick.Controls

Rectangle {
    width: 500
    height: 500

    Image {
        x: 0
        y: 0
        width: 36
        height: 35
        source: 'rcc_/icons/material/36x36/chevron-right-black.png'
    }

    Button {
        x: 100
        y: 100
        icon.source: Qt.resolvedUrl('rcc_/icons/material/36x36/chevron-right-black.png')
    }
}

// pyside6-qml flexbox.qml

import QtQuick
import QtQuick.Layouts

Window {
    id: root
    visible: true

    FlexboxLayout {
        id: flexLayout
        anchors.fill: parent
        wrap: FlexboxLayout.Wrap
        direction: FlexboxLayout.Row
        // justifyContent: FlexboxLayout.JustifySpaceAround
        justifyContent: FlexboxLayout.JustifyStart

        Rectangle {
            color: 'teal'
            implicitWidth: 200
            implicitHeight: 200
        }
        Rectangle {
            color: 'plum'
            Layout.fillWidth: true
            implicitWidth: 200
            implicitHeight: 200
        }
        /*
        Rectangle {
            color: 'olive'
            implicitWidth: 200
            implicitHeight: 200
        }
        Rectangle {
            color: 'beige'
            implicitWidth: 200
            implicitHeight: 200
        }
        Rectangle {
            color: 'darkseagreen'
            implicitWidth: 200
            implicitHeight: 200
        }
*/
    }
}

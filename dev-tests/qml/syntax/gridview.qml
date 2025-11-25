import QtQuick
import QtQuick.Controls

Window {
    id: root
    visible: true

    // The Repeater type creates all of its delegate items when the
    // repeater is first created.

    // This can be inefficient if there are a large number of delegate
    // items and not all of the items are required to be visible at
    // the same time.

    // If this is the case, consider using other view types like
    // ListView (which only creates delegate items when they are
    // scrolled into view) or use the Dynamic Object Creation methods
    // to create items as they are required.

    GridView {
        anchors.fill: parent
        anchors.margins: 10
        cellHeight: 60
        cellWidth: 60

        model: 200
        delegate: Item {
            // created/destroyed on demand
            // don't save state here !
            width: 50
            height: 50

            Rectangle {
                anchors.fill: parent
                color: Qt.rgba(Math.random(), Math.random(), Math.random(), 1)
            }

            Text {
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                text: modelData
            }

            Component.onCompleted: {
                console.info("delegate completed +", modelData)
            }
            Component.onDestruction: {
                console.info("delegate destroyed -", modelData)
            }
        }
    }
}

import QtQuick
import QtQuick.Controls

Window {
    id: root
    visible: true

    Rectangle {
        width: 300
        height: 300
        color: 'green'

        Text {
            id: myText
            anchors.fill: parent
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: 'Click anywhere'
        }

        WorkerScript {
            id: myWorker
            source: "script.mjs"

            onMessage: (messageObject) => myText.text = messageObject.reply
        }

        MouseArea {
            anchors.fill: parent
            onClicked: (mouse) => myWorker.sendMessage({ 'x': mouse.x, 'y': mouse.y })
        }
    }
}

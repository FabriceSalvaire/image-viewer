// pragma ComponentBehavior: Bound

import QtQuick

Window {
    id: root
    visible: true

    // required property int thing
    property int thing: 123

    Text {
        anchors.fill: parent
        text: "The thing is " + root.thing
    }

    component Inner: QtObject {
        objectName: "I can see " + root.thing + " because I'm bound."
    }

    component MyRectangle: Rectangle {
        width: root.thing
        height: 50
        color: 'blue'
    }

    MyRectangle {
        x: 10
        y: 100
    }

    Inner {
    }
}

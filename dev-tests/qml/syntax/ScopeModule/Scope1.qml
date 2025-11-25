import QtQuick

// p1 and root_rectangle1 are resolved from parent

Rectangle {
    id: rectangle1
    // color: 'green'
    color: root_rectangle1.color
    width: 100
    height: 50

    Component.onCompleted: {
        console.info('Scope1.onCompleted', p1, root_rectangle1.color)
        // qml: Scope1.onCompleted 123 #ff0000
    }
}

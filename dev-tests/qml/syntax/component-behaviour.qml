// https://doc.qt.io/qt-6/qtqml-documents-structure.html#componentbehavior

// pragma ComponentBehavior: Unbound
// default
//
// log:
//      qml: color.r 1
//      qml: color.g 1
// color is binded to Rectangle.color property

pragma ComponentBehavior: Bound
// in case of name clashes,
// IDs defined outside a bound component override local properties of objects created from the component
//
// log:
//      qml: color.r 12
//      qml: color.g undefined
// color is binded to ListView id

import QtQuick

ListView {
    id: color

    property int r: 12

    model: 1

    delegate: Rectangle {
        Component.onCompleted: {
            console.info('color.r', color.r)
            console.info('color.g', color.g)
        }
    }
}

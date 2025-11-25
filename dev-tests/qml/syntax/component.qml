// https://doc.qt.io/qt-6/qml-qtqml-component.html
// https://doc.qt.io/qt-6/qtqml-documents-definetypes.html#inline-components

import QtQuick

Window {
    id: root
    visible: true

    property Component mycomponent: comp1

    QtObject {
        id: internalSettings

        property color color: 'green'
    }

    Component {
        id: comp1

        Rectangle {
            color: internalSettings.color
            width: 400
            height: 10
        }
    }

    ListView {
        width: 400
        height: 400
        spacing: 10
        model: 5
        delegate: comp1
        // delegate: mycomponent   // using property
        // delegate: myItem.mycomponent   // using MyItem.qml

        // MyItem { id: myItem }
    }

    // inline component
    // component <component name> : BaseType {
    component MyRectangle: Rectangle {
        width: 100
        height: 50
        color: 'blue'
    }

    MyRectangle {
        x: 10
        y: 100
    }

    Rectangle {
        x: 10
        y: 300

        property alias caption: image.caption
        // property alias source: image.source

        Component1.LabeledImage {
            id: image
            caption: 'image'

            // log:
            //   qml: message isundefined
        }
    }

    Component1 {
        x: 200
        y: 300

        // log:
        //   qml: message is From Component1
        //   qml: message is From Component1
    }
}

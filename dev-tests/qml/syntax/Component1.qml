import QtQuick

Item {
    id: root

    property string message: "From Component1"

    // Inline component
    component LabeledImage: Column {
        // property alias source: image.source
        property alias caption: text.text
        spacing: 10

        Rectangle {
            id: image
            width: 50
            height: 50
            color: 'orange'
        }

        Text {
            id: text
            font.bold: true
        }

        // Inline components don't share their scope with the component they are declared in
        Component.onCompleted: console.info("message is", root.message)
    }

    Row {
        spacing: 10

        LabeledImage {
            id: before
            caption: "Before"
        }

        LabeledImage {
            id: after
            caption: "After"
        }

        Component2 {
        }

        // log:
        //   qml: message is From Component1
        //   qml: message is From Component1
    }

    property LabeledImage selectedImage: before
}

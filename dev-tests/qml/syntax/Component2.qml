import QtQuick

Rectangle {
    id: root2

    width: 50
    height: 50
    color: 'violet'

    // if `root2` id doesn't clash with `root`
    // QML will search for `root` in the context hierarchy
    Component.onCompleted: console.info("Component2: message is", root.message)
}

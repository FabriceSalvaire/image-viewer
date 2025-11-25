import QtQuick

import ScopeModule

Window {
    id: root
    visible: true

    property int p1: 123

    Rectangle {
        id: root_rectangle1
        color: 'red'
    }

    Scope1 {
        x: 10
        y: 10
    }
}

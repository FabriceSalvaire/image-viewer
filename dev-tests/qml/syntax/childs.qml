import QtQuick
import QtQuick.Controls

Window {
    id: root
    visible: true

    component MyRectangle: Rectangle {
        width: 100
        height: 50
        color: 'blue'
    }

    property Component mycomponent: MyRectangle {}

    Column {
        id: container
        x: 10
        y: 10
        spacing: 10

        children: [
            MyRectangle {
                color: 'red'
            },
            MyRectangle {
                color: 'green'
            },
            MyRectangle {
                color: 'blue'
            },
            MyRectangle {
                color: 'orange'
            }
        ]
    }

    Button {
        x: 300
        y: 10
        text: 'rotate'
        onClicked: {
            // container.dumpItemTree()
            var childs = container.children
            console.info(childs)
            var n = childs.length
            var indexes = []
            for (var i = 0; i < n; i++)
                indexes.push(i)
            var j = Math.trunc(n / 2) + 1
            console.info('rotate', j, n)
            indexes = indexes.slice(j, n).concat(indexes.slice(0, j))
            var sorted_childs = []
            indexes.forEach((i) => {sorted_childs.push(childs[i])})
            container.children = sorted_childs
            if (n < 6)
                mycomponent.createObject(
                    container,
                    {
                        color: Qt.rgba(Math.random(), Math.random(), Math.random(), 1)
                    }
                )
        }
    }
}

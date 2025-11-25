// pyside6-qml flexbox.qml
// https://qt-project.atlassian.net/browse/QTBUG-142033
//   The inline component in the FunctionFilter limits the qml file name

import QtQuick
import QtQml.Models

Window {
    id: root
    visible: true

    ListModel {
        id: listModel
        ListElement { name: "Adan"; age: 25; department: "Process"; pid: 209711; country: "Norway" }
        ListElement { name: "Hannah"; age: 48; department: "HR"; pid: 154916; country: "Germany" }
        ListElement { name: "Divina"; age: 63; department: "Marketing"; pid: 158038; country: "Spain" }
        ListElement { name: "Rohith"; age: 35; department: "Process"; pid: 202582; country: "India" }
        ListElement { name: "Latesha"; age: 23; department: "Quality"; pid: 232582; country: "UK" }
    }

    SortFilterProxyModel {
        id: ageFilterModel
        model: listModel
        filters: [
            FunctionFilter {
                id: functionFilter
                property int ageLimit: 20
                // typo qt doc
                // https://qt-project.atlassian.net/browse/QTBUG-142033
                component RoleData: QtObject {
                    property int age
                }
                // typo qt doc
                function filter(data: RoleData) : bool {
                    return data.age > ageLimit
                }
            }
        ]
        sorters: [
            RoleSorter { roleName: "department" }
        ]
    }

    ListView {
        anchors.fill: parent
        anchors.margins: 10
        clip: true
        model: ageFilterModel
        // model: listModel
        spacing: 10

        delegate: Rectangle {
            implicitWidth: 100
            implicitHeight: 50
            border.width: 1
            Text {
                text: name
                anchors.centerIn: parent
            }
        }
    }
}

Item {
    /********************************************************************************/
    // id convention

    // id: root

    Item {
        // id: _[componentName]_[componentDescription]
        id: _item_container
    }

    /********************************************************************************/

    // https://doc.qt.io/qt-6/qtqml-syntax-objectattributes.html
    // [default] [final] [required] [readonly] property <propertyType> <propertyName> : <value>

    // Default property
    //  An object definition can have a single default property
    default property var some_text
    // Usage:
    //   Foo {
    //       Text { text: "..." }
    //       // same as
    //       some_text: Text { text: "..." }
    //   }
    //
    // For Item, `data` property is the default
    //   Item {
    //       Text {}
    //       Rectangle {}
    //       Timer {}
    //   }
    // same as
    //   Item {
    //       data: [
    //           Text {},
    //           Rectangle {},
    //           Timer {}
    //       ]
    //   }
    // and (visual and resource dispatch)
    //   Item {
    //       children: [
    //           Text {},
    //           Rectangle {}
    //       ]
    //       resources: [
    //           Timer {}
    //       ]
    //   }

    // final keyword prohibits any shadowing of a property
    //   By default, properties can be shadowed: You can re-declare a
    //   property in a derived QML type, possibly with a new type and
    //   new attributes.
    //   The result will be two properties of the same name, only one of
    //   which is accessible in any given context.

    // required properties must be set when an instance of the object is created
    required property int some_number1
    required x   // Item.x

    // Constant
    readonly property int constant1 : 123

    // https://doc.qt.io/qt-6/qtqml-typesystem-valuetypes.html

    // Built-in value types
    property bool soom_bool
    property date some_date
    property double dome_double
    property int some_number
    property list some_list // List of QML objects
    property real some_real // Number with a decimal point
    property string some_string
    property url some_url

    // generic placeholder type
    property var some_number2: 1.5
    // variant = var type
    //   Use var instead

    // Empty value type
    // function do() : void {}
    // cannot declare: property void ...

    // QtQml types
    // point
    // rect
    // size

    // QtQuick types
    property color some_color
    // font
    // matrix4x4
    // quaternion
    // vector2d
    // vector3d
    // vector4d

    /********************************************************************************/

    // any QML object type can be used as a property type
    property Component mycomponent: comp1

    QtObject {
        id: internalSettings
        property color color: "green"
    }

    Component {
        id: comp1
        Rectangle {
            color: internalSettings.color
            width: 400
            height: 50
        }
    }

    /********************************************************************************/
    // Property Modifier Objects

    // <PropertyModifierTypeName> on <propertyName> {
    //   attributes of the object instance
    // }

    // NumberAnimation on x { ... }

    /********************************************************************************/
    // Signal Attributes

    // signal <signalName>[([<parameterName>: <parameterType>[, ...]])]
    signal clicked
    signal hovered()
    signal action_performed(action: string, action_result: int)

    onAction_performed: (action, action_result) => { ... }

    /********************************************************************************/
    // Property Change Signals

    onSomePropertyChanged: console.info('...')

    /********************************************************************************/
    // Method Attributes

    // function <functionName>([<parameterName>[: <parameterType>][, ...]]) [: <returnType>] { <body> }

    /********************************************************************************/
    // Attached Properties and Attached Signal Handlers

    // Attached properties and attached signal handlers are mechanisms
    // that enable objects to be annotated with extra properties or
    // signal handlers that are otherwise unavailable to the object.

    // In particular, they allow objects to access properties or
    // signals that are specifically relevant to the individual
    // object.

    // The instance of the attaching type is only attached to specific
    // objects, not to the object and all of its children.

    // <AttachingType>.<propertyName>
    //   ListView.isCurrentItem

    // <AttachingType>.on<SignalName>
    //   Component.onCompleted

    /********************************************************************************/
    // Enumeration Attributes
    //   https://doc.qt.io/qt-6/qtqml-typesystem-enumerations.html
    //   https://doc.qt.io/qtforpython-6/PySide6/QtCore/QEnum.html

    //   https://qml.guide/enums-in-qt-qml
    //   https://github.com/ndesai/qml.guide/tree/master/examples/QtQmlEnums
 
   enum TextType {
        Normal, // = 0
        Heading, // = 1
        Paragraph = 100,
        ParagraphBis = 100
    }

    property int textType: TextType.Normal

    // Qt.enumStringToValue(TextType, 'Normal')            -> 0
    // Qt.enumValueToString(TextType, TextType.Normal)     -> 'Normal'
    // Qt.enumValueToStrings(TextType, TextType.Paragraph) -> ['Paragraph', 'ParagraphBis']
}

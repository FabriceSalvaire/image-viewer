import QtQuick

Rectangle {
    height: 500
    width: 500

    Rectangle {
        id: stars
        x: 50
        y: 50
        height: 50

        property int number_of_stars: 5
        property bool half: false

        width: height * number_of_stars

        property real value: 0
        property real icon_value: 0

        function compute_value(x: real) : real {
            if (half)
                return Math.ceil((x * 2 * number_of_stars) / width) / 2
            else
                return Math.ceil((x * number_of_stars) / width)
        }

        function hover_star(x: real) {
            stars.icon_value = compute_value(x)
            console.info('hover_star', x, icon_value)
        }

        Row {
            id: star_row
            anchors.fill: parent
            spacing: 0

            Repeater {
                model: stars.number_of_stars

                Image {
                    width: stars.height
                    height: width
                    source: get_icon(stars.icon_value)

                    function get_icon(icon_value: real) : string {
                        var _ = icon_value - modelData
                        return _ > 0 ? (_ > .5 ? 'rcc_/icons/material/40x40/star-black.png' : 'rcc_/icons/material/40x40/star-half-white.png') : 'rcc_/icons/material/40x40/star-white.png'
                    }
                }
            }
        }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            onEntered: {
                console.info('onEntered', mouseX)
                stars.hover_star(mouseX)
            }
            onPositionChanged: (event) => {
                console.info('onPositionChanged', event.x)
                stars.hover_star(event.x)
            }
            onExited: {
                console.info('onExited')
                stars.icon_value = stars.value
            }
            onClicked: (event) => {
                console.info('onClicked', event.x)
                var _ = stars.compute_value(event.x)
                stars.value = _
                stars.icon_value = _
                console.info('star value', stars.value, _)
            }
        }
    }
}

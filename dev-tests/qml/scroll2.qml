import QtQuick

Rectangle {
    width: 500
    height: 500

    Timer {
        id: timer
        running: false
        repeat: true

        property real dt: 100 / 1000
        // property real deceleration: 3 * dt
        property real deceleration: .1

        property real speed: 0
        property int step: 0

        interval: dt * 1000 // ms

        onTriggered: {
            step += 1
            // var di = Math.abs(speed) - deceleration * dt * (step + 1/2)
            // var di = Math.abs(speed) - deceleration * (step + 1/2)
            var di = Math.abs(speed) - deceleration * step
            console.info('timer di dec', di, deceleration)
            if (di > 0) {
                var dx = di * dt
                // var dx = di
                if (speed < 0)
                    dx *= -1
                console.info('timer di dx', di, dx)
                target.y += dx
            }
            else
                stop()
        }
    }

    MouseArea {
        // don't implement WheelHandler.active
        anchors.fill: parent
        enabled: !handler.enabled
        onClicked: { parent.color = 'red' }
        onWheel: (wheel) => {
            console.info('mouse area wheel', Date.now(), wheel.x, wheel.y, wheel.angleDelta, wheel.pixelDelta)
        }
    }

    TapHandler {
        // tap doesn't work
        acceptedDevices: PointerDevice.Mouse | PointerDevice.TouchPad | PointerDevice.Stylus
        onTapped: {
            console.info('tap')
            timer.stop()
        }
    }

    WheelHandler {
        id: handler
        enabled: true
        acceptedDevices: PointerDevice.TouchPad // mouse and pad

        property real last_position
        property real last_speed

        onWheel: (wheel) => {
          console.info('wheel handler', Date.now(), wheel.x, wheel.y, wheel.angleDelta, wheel.pixelDelta)
          last_position = target.y
          target.y = last_position - wheel.pixelDelta.y
          var speed = target.y - last_position
          if (speed != 0)
              last_speed = speed
          console.info('wheel handler', target.y, last_position, last_speed)
        }

        onActiveChanged: {
            console.info('wheel handler   active=', active, 'speed=', last_speed)
            timer.speed = last_speed
            timer.step = 0
            timer.start()
        }
    }

    Item {
        id: target
        x: 200
        y: 200

        Column {
            spacing: 10

            Repeater {
                model: 10

                Rectangle {
                    x: 0
                    y: 0
                    width: 200
                    height: 20
                    color: Qt.rgba(Math.random(), Math.random(), Math.random(), 1)
                    antialiasing: true
                    focus: true
                }
            }
        }
    }
}

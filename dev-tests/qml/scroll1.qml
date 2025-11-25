import QtQuick

Rectangle {
    width: 500
    height: 500

    Component.onCompleted: {
        console.info("completed")
    }

    Rectangle {
        id: target
        x: 200
        y: 200
        width: 200
        height: 200
        color: "green"
        antialiasing: true
        focus: true

        MouseArea {
            // don't implement WheelHandler.active
            anchors.fill: parent
            enabled: !handler.enabled
            onClicked: { parent.color = 'red' }
            onWheel: (wheel) => {
                console.info('mouse area wheel', Date.now(), wheel.x, wheel.y, wheel.angleDelta, wheel.pixelDelta)
                parent.rotation += wheel.angleDelta.y / 120 * 10
            }
        }

        Timer {
            id: timer
            running: false
            repeat: true

            property real dt: 100 / 1000
            // property real deceleration: 3 * dt
            property real deceleration: 1

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
                    target.rotation += dx
                    // target.y += dx
                }
                else
                    stop()
            }
        }

        TapHandler {
            // tap doesn't work
            acceptedDevices: PointerDevice.Mouse | PointerDevice.TouchPad | PointerDevice.Stylus
            // gesturePolicy: TapHandler.ReleaseWithinBounds
            onTapped: {
                console.info('tap')
                timer.stop()
            }
        }

        WheelHandler {
            id: handler
            enabled: true
            // By default, this property is set to PointerDevice.Mouse
            // acceptedDevices: PointerDevice.Mouse | PointerDevice.TouchPad
            // acceptedDevices: PointerDevice.Mouse // do nothing
            acceptedDevices: PointerDevice.TouchPad // mouse and pad
            // property: 'rotation'
            property real last_position
            property real speed
            onWheel: (wheel) => {
                last_position = target.rotation
                console.info('wheel handler', Date.now(), wheel.x, wheel.y, wheel.angleDelta, wheel.pixelDelta)
                target.rotation = last_position - wheel.pixelDelta.y
                var cspeed = target.rotation - last_position
                if (cspeed != 0)
                    speed = cspeed
                console.info('wheel handler', target.rotation, last_position, speed)
                }
            /*
            onWheel: (wheel) => {
                last_position = target.y
                console.info('wheel handler', Date.now(), wheel.x, wheel.y, wheel.angleDelta, wheel.pixelDelta)
                target.y = last_position - wheel.pixelDelta.y
                var cspeed = target.y - last_position
                if (cspeed != 0)
                    speed = cspeed
                console.info('wheel handler', target.y, last_position, speed)
            }
            */
            onActiveChanged: {
                console.info('wheel handler   active=', active)
                console.info('wheel handler speed', speed)
                timer.speed = speed
                timer.step = 0
                timer.start()
            }
        }
    }
}

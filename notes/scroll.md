# Firefox

about:support
-> wayland

synthesise a tap to stop kinematic scrolling ???

# Sliding physics

Force de friction Ff = μFn où Fn = P = mg
Ff = μmg

équation dynamique
ma = -μmg -> a = dV/dt = -μg = cst = -C
v(t) = V0 -C t tant que V >= 0 soit t <= V0/C
x(t) = X0 + V0 t -C t**2/2
d = V0**2 / 2C

travail
W = Ff d = μmg d = m/2 V0**2 = Cm d
d = V0**2 / 2μg

variationnel
D1 = V0  dt -C/2    dt**2
D2 = V0 2dt -C/2 (2dt)**2
D3 = V0 3dt -C/2 (3dt)**2

i dt <= V0/C -> i = V0/(C dt)

di = D(i) - D(i-1)
di = V0 dt -C/2 (2i + 1) dt**2
di = (V0 -C/2 (2i + 1) dt ) dt
di = (V0 -C (i + 1/2) dt ) dt   tant que > 0

timer tous les dt
di décroît -> 0
stop @ di < 0

scroll dt drives target
compute V
when WheelHandler.activer -> false
start timer

# Qt

```
qt.qpa.wayland.input: Axis source finger
qt.qpa.wayland.input: wl_pointer.axis vertical: 3.15625
qt.qpa.wayland.input: Flushing scroll event sending ScrollBegin
qt.qpa.wayland.input: Flushing scroll event Qt::ScrollUpdate QPoint(0,-3) QPoint(0,-38)
...
qt.qpa.wayland.input: Axis source finger
qt.qpa.wayland.input: wl_pointer.axis vertical: -0.261719
qt.qpa.wayland.input: Flushing scroll event Qt::ScrollUpdate QPoint(0,0) QPoint(0,3)

qt.qpa.wayland.input: Axis source finger
qt.qpa.wayland.input: Received horizontal wl_pointer.axis_stop

qt.qpa.wayland.input: Axis source finger
qt.qpa.wayland.input: Received vertical wl_pointer.axis_stop
```

`qtbase/src/plugins/platforms/wayland/qwaylandinputdevice.cpp`

# Wayland

---

[Appendix A. Wayland Protocol Specification](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_pointer-enum-axis)

---

```
[3923763.610] {Default Queue} wl_pointer#29.axis_source(1)
[3923763.626] {Default Queue} wl_pointer#29.axis_relative_direction(0, 0)
[3923763.629] {Default Queue} wl_pointer#29.axis(8277724, 0, -1.05078125)
[3923763.633] {Default Queue} wl_pointer#29.frame()

[3923773.096] {Default Queue} wl_pointer#29.axis_source(1)
[3923773.104] {Default Queue} wl_pointer#29.axis_stop(8277733, 1)
[3923773.119] {Default Queue} wl_pointer#29.axis_source(1)
[3923773.124] {Default Queue} wl_pointer#29.axis_stop(8277733, 0)
[3923773.128] {Default Queue} wl_pointer#29.frame()
```

`wl_pointer::axis` - axis event
time
    uint - timestamp with millisecond granularity
axis
    `wl_pointer::axis` (uint) - axis type
value
    fixed - length of vector in surface-local coordinate space
Scroll and other axis notifications.
For scroll events (vertical and horizontal scroll axes), the value parameter is the **length of a
vector** along the specified axis in a coordinate space identical to those of motion events,
representing a relative movement along the specified axis.
For devices that support movements non-parallel to axes multiple axis events will be emitted.
When applicable, for example for touch pads, the server can choose to emit scroll events where the
motion vector is equivalent to a motion event vector.
When applicable, a client can transform its content relative to the scroll distance. 


`wl_pointer::frame` - end of a pointer event sequence


`wl_pointer::axis_source` - axis source event
`axis_source`
    `wl_pointer::axis_source` (uint) - source of the axis event
Source information for scroll and other axes.
This event does not occur on its own. It is sent before a `wl_pointer.frame` event and carries the
source information for all events within that frame.


`wl_pointer::axis_stop` - axis stop event
`time`
    uint - timestamp with millisecond granularity
`axis`
    `wl_pointer::axis` (uint) - the axis stopped with this event
Stop notification for scroll and other axes.


`wl_pointer::axis_relative_direction` - axis relative physical direction event
axis
    `wl_pointer::axis` (uint) - axis type
direction
    `wl_pointer::axis_relative_direction` (uint) - physical direction relative to axis motion
Relative directional information of the entity causing the axis motion.

---

`wl_pointer::axis` - axis types
Describes the axis types of scroll events.
`vertical_scroll`
    0 - vertical axis
`horizontal_scroll`
    1 - horizontal axis


`wl_pointer::axis_source` - axis source types
Describes the source types for axis events. This indicates to the client how an axis event was
physically generated; a client may adjust the user interface accordingly. For example, scroll events
from a "finger" source may be in a smooth coordinate space with kinetic scrolling whereas a "wheel"
source may be in discrete steps of a number of lines.
The "continuous" axis source is a device generating events in a continuous coordinate space, but
using something other than a finger. One example for this source is button-based scrolling where the
vertical motion of a device is converted to scroll events while a button is held down.
The "wheel tilt" axis source indicates that the actual device is a wheel but the scroll event is not
caused by a rotation but a (usually sideways) tilt of the wheel.
`wheel`
    0 - a physical wheel rotation
`finger`
    1 - finger on a touch surface
`continuous`
    2 - continuous coordinate space
`wheel_tilt`
    3 - a physical wheel tilt


`wl_pointer::axis_relative_direction` - axis relative direction
This specifies the direction of the physical motion that caused a `wl_pointer.axis` event, relative to
the `wl_pointer.axis` direction.
`identical`
    0 - physical motion matches axis direction
`inverted`
    1 - physical motion is the inverse of the axis direction

from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait
from usys import stdin, stdout
from uselect import poll

MOTOR_SPEED = 10

hub = TechnicHub()
motor = Motor(Port.A)

keyboard = poll()
keyboard.register(stdin)
hub.light.on(Color.YELLOW)
while True:
    stdout.buffer.write(b"rdy")

    while not keyboard.poll(0):
        wait(10)

    cmd = stdin.buffer.read(3)

    if cmd == b"fwd":
        motor.dc(MOTOR_SPEED)
        stdout.buffer.write(b"OK")
    elif cmd == b"rev":
        motor.dc(-MOTOR_SPEED)
        stdout.buffer.write(b"OK")
    elif cmd == b"bye":
        break
    else:
        motor.stop()

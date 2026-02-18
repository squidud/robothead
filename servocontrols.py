from gpiozero import AngularServo
from time import sleep

# Create servos on different GPIO pins
eyeslr = AngularServo(12)  # eyes l/r
eyesud = AngularServo(13)  # eyes up/down
jaw = AngularServo(18)  # jaw
necklr = AngularServo(19)   # neck l/r

# Control them using angles
eyeslr.angle = 0
eyesud.angle = 0
jaw.angle = 0
necklr.angle = 0

sleep(1)

while True:
    eyeslr.angle = -90
    sleep(0.9)

    eyeslr.angle = 90
    sleep(0.9)

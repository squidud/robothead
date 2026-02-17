from gpiozero import AngularServo
from time import sleep

# Create servos on different GPIO pins
eyeslr = AngularServo(17)  # eyes l/r
eyesud = AngularServo(27)  # eyes up/down
jaw = AngularServo(22)  # jaw
necklr = AngularServo(5)   # neck l/r

# Control them using angles (0-180 degrees)
eyeslr.angle = 90  
eyesud.angle = 90   
jaw.angle = 90    
necklr.angle = 90   

sleep(2)

while True:
    eyeslr.angle = 0 
    sleep(0.7)

    eyeslr.angle = 180
    sleep(0.7)


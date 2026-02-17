from gpiozero import AngularServo
from time import sleep

# Create servos on different GPIO pins
eyeslr = AngularServo(17, min_angle=0, max_angle=180)  # eyes l/r
eyesud = AngularServo(27, min_angle=0, max_angle=180)  # eyes up/down
jaw = AngularServo(22, min_angle=0, max_angle=180)  # jaw
necklr = AngularServo(5, min_angle=0, max_angle=180)   # neck l/r

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


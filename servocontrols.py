from gpiozero import AngularServo, Device
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
# Try to use pigpio for hardware-timed PWM (reduces jitter). Falls back if unavailable.
try:
    Device.pin_factory = PiGPIOFactory()
except Exception:
    pass

# Create servos on different GPIO pins. Specify angle range and pulse widths.
# Typical hobby servos respond around 1-2 ms; some work better with 0.5-2.5 ms.
PULSE_MIN = 0.0005
PULSE_MAX = 0.0025

eyeslr = AngularServo(17, min_angle=0, max_angle=180,
                      min_pulse_width=PULSE_MIN, max_pulse_width=PULSE_MAX)  # eyes l/r
eyesud = AngularServo(27, min_angle=0, max_angle=180,
                      min_pulse_width=PULSE_MIN, max_pulse_width=PULSE_MAX)  # eyes up/down
jaw = AngularServo(22, min_angle=0, max_angle=180,
                  min_pulse_width=PULSE_MIN, max_pulse_width=PULSE_MAX)  # jaw
necklr = AngularServo(5, min_angle=0, max_angle=180,
                     min_pulse_width=PULSE_MIN, max_pulse_width=PULSE_MAX)   # neck l/r
# Control them using angles (0-180 degrees)
eyeslr.angle = 90
eyesud.angle = 90
jaw.angle = 90
necklr.angle = 90

sleep(2)

def move_smooth(servo, target, step=3, delay=0.02):
    """Move `servo` smoothly from its current angle to `target`.

    step: degrees per iteration (smaller = smoother)
    delay: seconds between steps
    """
    try:
        current = servo.angle if servo.angle is not None else 90
    except Exception:
        current = 90
    if current == target:
        return
    direction = 1 if target > current else -1
    for a in range(int(current), int(target), direction * int(step)):
        servo.angle = a
        sleep(delay)
    servo.angle = target

move_smooth(eyeslr, 0, step=4, delay=0.02)

# Example loop using smoothing. Reduce `step` or `delay` for smoother motion.
while True:
    move_smooth(eyesud, 180, step=4, delay=0.02)
    sleep(0.8)
    move_smooth(eyeslr, 180, step=4, delay=0.02)
    sleep(0.8)
    move_smooth(eyesud, 0, step=4, delay=0.02)
    sleep(0.8)
    move_smooth(eyeslr, 0, step=4, delay=0.02)
    


# Notes:
# - If jitter persists, ensure a solid 5V power supply with common ground to the Pi.
# - Add a 470-1000uF electrolytic across the servo supply near the servos.
# - For many servos, consider a PCA9685 controller (I2C) to offload PWM.
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


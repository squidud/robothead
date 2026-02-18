from rpi_hardware_pwm import HardwarePWM
from time import sleep

SERVO_HZ = 50
MIN_DUTY = 2.5   # 0.5ms pulse = 0 degrees
MAX_DUTY = 12.5  # 2.5ms pulse = 180 degrees

def angle_to_duty(angle):
    return MIN_DUTY + (angle / 180.0) * (MAX_DUTY - MIN_DUTY)

# Pi 5 hardware PWM - each dtoverlay creates a chip with 2 channels
# chip 0, channels 0-1 = GPIO 12, 13
# chip 1, channels 0-1 = GPIO 18, 19
eyeslr = HardwarePWM(pwm_channel=0, hz=SERVO_HZ, chip=0)  # GPIO 12 - eyes l/r
eyesud = HardwarePWM(pwm_channel=1, hz=SERVO_HZ, chip=0)  # GPIO 13 - eyes up/down
jaw = HardwarePWM(pwm_channel=0, hz=SERVO_HZ, chip=1)     # GPIO 18 - jaw
necklr = HardwarePWM(pwm_channel=1, hz=SERVO_HZ, chip=1)  # GPIO 19 - neck l/r

# Start all servos at 90 degrees
print("Starting servos...")
eyeslr.start(angle_to_duty(90))
eyesud.start(angle_to_duty(90))
jaw.start(angle_to_duty(90))
necklr.start(angle_to_duty(90))

sleep(1)

try:
    while True:
        print("Moving to 0")
        eyeslr.change_duty_cycle(angle_to_duty(0))
        sleep(0.9)

        print("Moving to 180")
        eyeslr.change_duty_cycle(angle_to_duty(180))
        sleep(0.9)
except KeyboardInterrupt:
    eyeslr.stop()
    eyesud.stop()
    jaw.stop()
    necklr.stop()

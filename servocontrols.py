import os
import subprocess
from time import sleep

CHIP_PATH = '/sys/class/pwm/pwmchip0'
PERIOD_NS = 20_000_000  # 20ms = 50Hz

# Pi 5 RP1 PWM0 pin mapping (from pinctrl funcs output)
# GPIO 12 = PWM0_CHAN0, alt 1
# GPIO 13 = PWM0_CHAN1, alt 1
# GPIO 18 = PWM0_CHAN2, alt 3
# GPIO 19 = PWM0_CHAN3, alt 3

def setup_pins():
    subprocess.run(['pinctrl', 'set', '12', 'a1'], check=True)
    subprocess.run(['pinctrl', 'set', '13', 'a1'], check=True)
    subprocess.run(['pinctrl', 'set', '18', 'a3'], check=True)
    subprocess.run(['pinctrl', 'set', '19', 'a3'], check=True)

def export_channel(channel):
    pwm_path = os.path.join(CHIP_PATH, f'pwm{channel}')
    if not os.path.exists(pwm_path):
        with open(os.path.join(CHIP_PATH, 'export'), 'w') as f:
            f.write(str(channel))
    with open(os.path.join(pwm_path, 'period'), 'w') as f:
        f.write(str(PERIOD_NS))
    with open(os.path.join(pwm_path, 'enable'), 'w') as f:
        f.write('1')
    return pwm_path

def set_angle(pwm_path, angle):
    pulse_ns = int(500_000 + (angle / 180.0) * 2_000_000)
    with open(os.path.join(pwm_path, 'duty_cycle'), 'w') as f:
        f.write(str(pulse_ns))

def cleanup(*paths):
    for p in paths:
        with open(os.path.join(p, 'enable'), 'w') as f:
            f.write('0')

setup_pins()

eyeslr = export_channel(0)   # GPIO 12 - eyes l/r
eyesud = export_channel(1)   # GPIO 13 - eyes up/down
jaw = export_channel(2)      # GPIO 18 - jaw
necklr = export_channel(3)   # GPIO 19 - neck l/r

print("Starting servos...")
set_angle(eyeslr, 90)
set_angle(eyesud, 90)
set_angle(jaw, 90)
set_angle(necklr, 90)

sleep(1)

try:
    while True:
        print("Moving to 0")
        set_angle(eyeslr, 0)
        sleep(0.9)

        print("Moving to 180")
        set_angle(eyeslr, 180)
        sleep(0.9)
except KeyboardInterrupt:
    cleanup(eyeslr, eyesud, jaw, necklr)

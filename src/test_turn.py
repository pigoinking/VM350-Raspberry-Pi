import RPi.GPIO as GPIO
from config import Config
from motion import Motion

config = Config()
motion = Motion(config)

dir = 1

try:

    # height restriction => color sign
    if dir == -1:
        motion.turn_left_motor()
    elif dir == 1:
        motion.turn_right_motor()
    else:
        # no color detected ever, something wrong
        raise KeyboardInterrupt

    # done
    motion.stop_motor()

except KeyboardInterrupt:
    GPIO.cleanup()
    print("GPIO Good to Go")

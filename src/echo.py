import RPi.GPIO as GPIO
from time import sleep, time

class Echo:
    def __init__(self, config):
        self.config = config
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(config.echo_trigPin,GPIO.OUT)
        GPIO.setup(config.echo_echoPin,GPIO.IN)

    def get_dist(self):
        # unit: cm
        GPIO.output(self.config.echo_trigPin, 0)
        sleep(2e-6)
        GPIO.output(self.config.echo_trigPin, 1)
        sleep(10e-6)
        GPIO.output(self.config.echo_trigPin, 0)
        while GPIO.input(self.config.echo_echoPin) == 0:
            pass
        start = time()
        while GPIO.input(self.config.echo_echoPin) == 1:
            pass
        stop = time()
        dist = (stop - start) * self.config.sound_speed
        return dist/2

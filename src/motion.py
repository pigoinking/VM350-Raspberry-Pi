import RPi.GPIO as GPIO
from time import sleep
import threading

class Motion:
    def __init__(self, config):
        GPIO.setmode(GPIO.BOARD)
        self.config = config
        # setup servo
        GPIO.setup(config.lbs, GPIO.OUT)
        self.lbs_pwm = GPIO.PWM(config.lbs, config.servo_freq)
        self.lbs_pwm.start(0)

        # setup servo
        GPIO.setup(config.rbs, GPIO.OUT)
        self.rbs_pwm = GPIO.PWM(config.rbs, config.servo_freq)
        self.rbs_pwm.start(0)

        # setup motor
        GPIO.setup(config.lm_in1, GPIO.OUT)
        GPIO.setup(config.lm_in2, GPIO.OUT)
        GPIO.setup(config.lm_en, GPIO.OUT)
        self.lm_pwm = GPIO.PWM(config.lm_en, config.motor_freq) # 100Hz
        self.lm_pwm.start(0)

        # setup motor
        GPIO.setup(config.rm_in1, GPIO.OUT)
        GPIO.setup(config.rm_in2, GPIO.OUT)
        GPIO.setup(config.rm_en, GPIO.OUT)
        self.rm_pwm = GPIO.PWM(config.rm_en, config.motor_freq) # 100Hz
        self.rm_pwm.start(0)

    def cleanup(self):
        for pwm in [self.lbs_pwm, self.rbs_pwm, self.lm_pwm, self.rm_pwm]:
            pwm.stop()

    def stop_motor(self):
        left_thread = threading.Thread(
            target=self.set_left_motor_speed,
            args=(0,),
        )
        right_thread = threading.Thread(
            target=self.set_right_motor_speed,
            args=(0,),
        )
        left_thread.start()
        right_thread.start()
        left_thread.join()
        right_thread.join()

    def forward_motor(self):
        left_thread = threading.Thread(
            target=self.set_left_motor_speed,
            args=(self.config.motor_speed,),
        )
        right_thread = threading.Thread(
            target=self.set_right_motor_speed,
            args=(self.config.motor_speed,),
        )
        left_thread.start()
        right_thread.start()
        left_thread.join()
        right_thread.join()
        
    def backward_motor(self):
        left_thread = threading.Thread(
            target=self.set_left_motor_speed,
            args=(-self.config.motor_speed,),
        )
        right_thread = threading.Thread(
            target=self.set_right_motor_speed,
            args=(-self.config.motor_speed,),
        )
        left_thread.start()
        right_thread.start()
        left_thread.join()
        right_thread.join()

    def turn_left_motor(self):
        self.set_left_motor_speed(0)
        self.set_right_motor_speed(self.config.motor_speed)
        sleep(self.config.motor_turn_time)
        self.stop_motor()

    def turn_right_motor(self):
        self.set_left_motor_speed(self.config.motor_speed)
        self.set_right_motor_speed(0)
        sleep(self.config.motor_turn_time)
        self.stop_motor()

    def expand_servo(self):

        def expand_once():
            left_thread = threading.Thread(
                target=self.set_left_servo_angle,
                args=(self.config.expand_left_servo_angle,),
            )
            right_thread = threading.Thread(
                target=self.set_right_servo_angle,
                args=(self.config.expand_right_servo_angle,),
            )
            left_thread.start()
            right_thread.start()
            left_thread.join()
            right_thread.join()

        expand_once()
        sleep(1)
        self.retract_servo()
        sleep(1)
        expand_once()

    def retract_servo(self):
        left_thread = threading.Thread(
            target=self.set_left_servo_angle,
            args=(self.config.retract_left_servo_angle,),
        )
        right_thread = threading.Thread(
            target=self.set_right_servo_angle,
            args=(self.config.retract_right_servo_angle,),
        )
        left_thread.start()
        right_thread.start()
        left_thread.join()
        right_thread.join()

    def set_left_servo_angle(self, angle):
        duty = angle / 18 + 2
        self.lbs_pwm.ChangeDutyCycle(duty)
        sleep(self.config.servo_angle_sleep)
        self.lbs_pwm.ChangeDutyCycle(0)

    def set_right_servo_angle(self, angle):
        duty = angle / 18 + 2
        self.rbs_pwm.ChangeDutyCycle(duty)
        sleep(self.config.servo_angle_sleep)
        self.rbs_pwm.ChangeDutyCycle(0)

    def set_left_motor_speed(self, speed):
        speed = -speed
        if speed > 0:
            GPIO.output(self.config.lm_in1, GPIO.HIGH)
            GPIO.output(self.config.lm_in2, GPIO.LOW)
            self.lm_pwm.ChangeDutyCycle(abs(speed))
        elif speed < 0:
            GPIO.output(self.config.lm_in1, GPIO.LOW)
            GPIO.output(self.config.lm_in2, GPIO.HIGH)
            self.lm_pwm.ChangeDutyCycle(abs(speed))
        else:
            GPIO.output(self.config.lm_in1, GPIO.LOW)
            GPIO.output(self.config.lm_in2, GPIO.LOW)
            self.lm_pwm.ChangeDutyCycle(0)

    def set_right_motor_speed(self, speed):
        if speed > 0:
            GPIO.output(self.config.rm_in1, GPIO.HIGH)
            GPIO.output(self.config.rm_in2, GPIO.LOW)
            self.rm_pwm.ChangeDutyCycle(abs(speed))
        elif speed < 0:
            GPIO.output(self.config.rm_in1, GPIO.LOW)
            GPIO.output(self.config.rm_in2, GPIO.HIGH)
            self.rm_pwm.ChangeDutyCycle(abs(speed))
        else:
            GPIO.output(self.config.rm_in1, GPIO.LOW)
            GPIO.output(self.config.rm_in2, GPIO.LOW)
            self.rm_pwm.ChangeDutyCycle(0)

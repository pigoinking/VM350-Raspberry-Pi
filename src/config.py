class Config:
    def __init__(self, is_front_echo = True):
        self.is_hardcode = True
        self.loop_sleep = 0.2

        self.lbs = 11 # left big motor, servo
        self.rbs = 12 # right big motor, servo
        self.lm_en = 31 # left motor EN pin
        self.rm_en = 32 # right motor EN pin
        self.lm_in1 = 35 # left motor in1
        self.lm_in2 = 36 # left motor in2
        self.rm_in1 = 37 # right motor in1
        self.rm_in2 = 38 # right motor in2

        self.servo_freq = 50
        self.motor_freq = 100
        self.servo_angle_sleep = 1
        self.expand_left_servo_angle = 50
        self.retract_left_servo_angle = 113
        self.expand_right_servo_angle = 80
        self.retract_right_servo_angle = 15
        self.motor_speed = 100

        self.motor_turn_time = 2.9 # time for motor to turn left / right

        if is_front_echo:
            self.echo_trigPin = 18
            self.echo_echoPin = 16
        else:
            self.echo_trigPin = 13
            self.echo_echoPin = 15

        self.sound_speed = 34300

        self.expand_dist = 15  # cm
        self.expand_time = 2 # s

        self.picam2_w = 1280
        self.picam2_h = 720
        self.hue_green = [30, 75]
        self.hue_red = [0, 10]
        self.sat_green = [100, 255]
        self.sat_red = [100, 255]

        self.retract_dist = 10  # cm, distance before retract (height restriction)

        self.turn_dist = 5 # cm, distance before turn

        # the time from turn -> parking = k * elapsed + b [in sec]
        # e.g. elapsed_k = 1, elapsed_b = 15
        self.elapsed_k = 5
        self.elapsed_b = 15

        self.check_sand_time = 2  # the time to check if it is in the sand area [in sec]
        self.check_off_sand_time = (
            0.6  # the time to check if it is off the sand area [in sec]
        )
        self.sand_front_dist = (
            50  # cm, the distance to check if it is in the sand area
        )
        self.off_sand_front_dist = (
            45  # cm, the distance to check if it is off the sand area
        )
        self.turn_side_dist = 70  # cm, the distance on the side to turn left / right

        self.stair_sand_time = 14

        self.park_time = 3 # the time to drive into parking area [in sec]

        self.colordetect_round = 21
        
        self.move_after_turn = 11

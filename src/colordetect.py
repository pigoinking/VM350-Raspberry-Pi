from time import sleep
import cv2
from picamera2 import Picamera2
import numpy as np

class ColorDetect:
    def __init__(self, config):
        self.config = config

        self.green_lb = np.array([config.hue_green[0], config.sat_green[0], 0])
        self.green_ub = np.array([config.hue_green[1], config.sat_green[1], 255])
        self.red_lb = np.array([config.hue_red[0], config.sat_red[0], 0])
        self.red_ub = np.array([config.hue_red[1], config.sat_red[1], 255])

        self.picam2 = Picamera2()
        # self.picam2.preview_configuration.main.size = (config.picam2_w, config.picam2_h)
        # self.picam2.preview_configuration.main.format = "RGB888"
        # self.picam2.preview_configuration.controls.FrameRate=30
        # self.picam2.preview_configuration.align()
        # self.picam2.configure("preview")
        self.picam2.start()

    def judge_color(self):
        # 0: nothing
        # -1: green on left
        # 1: green on right
        frame = self.picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        green_mask = cv2.inRange(frame, self.green_lb, self.green_ub)
        red_mask = cv2.inRange(frame, self.red_lb, self.red_ub)
        if cv2.countNonZero(green_mask) and cv2.countNonZero(red_mask):
            gx, _, gw, _ = cv2.boundingRect(sorted(cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0], key=cv2.contourArea, reverse=True)[0])
            rx, _, rw, _ = cv2.boundingRect(sorted(cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0], key=cv2.contourArea, reverse=True)[0])
            if gx + gw / 2 < rx + rw / 2:
                return 1
            else:
                return -1
        return 0

    def judge_color_stable(self):
        cnt = 0
        for _ in range(self.config.colordetect_round):
            color = 0
            while color == 0:
                color = self.judge_color()
            cnt += color
            print(cnt, color)
            sleep(0.1)
        print(cnt)
        if cnt > 0:
            return 1
        if cnt < 0:
            return -1
        return 0  

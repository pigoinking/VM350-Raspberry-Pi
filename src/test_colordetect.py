from config import Config
from colordetect import ColorDetect

dir = 0 # left: -1, right: 1

def record_color():
    try:
        global dir
        # if dir:
        #    return
        color = colordetect.judge_color()
        # if color:
        dir = color
    except OSError:
        pass

config = Config()
colordetect = ColorDetect(config)

while True:
    record_color()
    print(dir)

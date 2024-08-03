import RPi.GPIO as GPIO
from config import Config
from motion import Motion
from echo import Echo
from colordetect import ColorDetect
from time import sleep, time

frontconfig = Config(is_front_echo=True)
sideconfig = Config(is_front_echo=False)
motion = Motion(frontconfig)
frontecho = Echo(frontconfig)
sideecho = Echo(sideconfig)
colordetect = ColorDetect(frontconfig)
dir = 0 # left: -1, right: 1


def record_color():
    global dir
    if dir:
        return
    color = colordetect.judge_color_stable()
    if color:
        dir = color

front_dist_history = []
side_dist_history = []

# 0 = beginning
# 1 = on the sand
# 2 = off the sand
status = 0

try:

    # start => 1st stair
    motion.forward_motor()
    start = time()
    while True:
        # record_color()
        front_dist = frontecho.get_dist()
        side_dist = sideecho.get_dist()
        print("Front: ", front_dist, "Side: ", side_dist)
        front_dist_history.append({"dist": front_dist, "time": time() - start})
        side_dist_history.append({"dist": side_dist, "time": time() - start})
        if front_dist < frontconfig.expand_dist:
            stop = time()
            motion.stop_motor()
            sleep(1)
            motion.forward_motor()
            sleep(1)
            motion.stop_motor()
            motion.backward_motor()
            sleep(1)
            motion.stop_motor()
            sleep(frontconfig.expand_time)
            motion.expand_servo()
            sleep(frontconfig.expand_time)
            break
        sleep(frontconfig.loop_sleep)
    elapsed = stop - start
    print("go!")

    # 1st stair => 2nd stair
    motion.forward_motor()

    if not frontconfig.is_hardcode:
        while True:
            front_dist = frontecho.get_dist()
            side_dist = sideecho.get_dist()
            print("Front: ", front_dist, "Side: ", side_dist)
            front_dist_history.append({"dist": front_dist, "time": time() - start})
            side_dist_history.append({"dist": side_dist, "time": time() - start})

            # check if it is in the sand area
            check_sand_num = frontconfig.check_sand_time / frontconfig.loop_sleep
            # check if it is off the sand area
            check_off_sand_num = (
                frontconfig.check_off_sand_time / frontconfig.loop_sleep
            )
            if status == 0:
                # check if the last check_num distances are all in the sand area
                if all(
                    [
                        item["dist"] > frontconfig.sand_front_dist
                        for item in front_dist_history[-int(check_sand_num) :]
                    ]
                ):
                    status = 1
            elif status == 1:
                # check if the last check_num distances are all off the sand area
                if all(
                    [
                        item["dist"] < frontconfig.off_sand_front_dist
                        for item in front_dist_history[-int(check_off_sand_num) :]
                    ]
                ):
                    status = 2

            if status == 2:
                motion.stop_motor()
                sleep(frontconfig.expand_time)
                motion.retract_servo()
                sleep(frontconfig.expand_time)
                motion.forward_motor()
                break
            print("Status: ", status)
            sleep(frontconfig.loop_sleep)
    else:
        sleep(frontconfig.stair_sand_time)
        motion.stop_motor()
        sleep(frontconfig.expand_time)
        motion.retract_servo()
        sleep(frontconfig.expand_time)
        motion.forward_motor()

    # check until reaches the color sign
    while True:
        side_dist = sideecho.get_dist()
        print("Side: ", side_dist)
        if side_dist > frontconfig.turn_side_dist:
            motion.stop_motor()
            print('stop')
            break
        sleep(frontconfig.loop_sleep)

    # check the color sign
    while True:
        record_color()
        if dir:
            break
    if dir == 1:
        print('left')
        motion.turn_right_motor()
    else:
        print('right')
        motion.turn_left_motor()
    print('forward')

    # global move_start
    # move_start = time()
    # while True:
    motion.forward_motor()
    sleep(frontconfig.move_after_turn)
    if dir == 1:
        print('left')
        motion.turn_right_motor()
    else:
        print('right')
        motion.turn_left_motor()

    motion.forward_motor()
    sleep(frontconfig.park_time)
    motion.stop_motor()

    # 2nd stair => height restriction
    # while True:
    #     # record_color()
    #     dist = echo.get_dist()
    #     if dist < config.retract_dist:
    #         motion.stop_motor()
    #         motion.retract_servo()
    #         sleep(config.expand_time)
    #         break
    #     sleep(config.loop_sleep)

    # height restriction => color sign
    # motion.forward_motor()
    # while True:
    #     record_color()
    #     dist = echo.get_dist()
    #     if dist < config.turn_dist:
    #         motion.stop_motor()
    #         if dir == -1:
    #             motion.turn_left_motor()
    #         elif dir == 1:
    #             motion.turn_right_motor()
    #         else:
    #             # no color detected ever, something wrong
    #             raise KeyboardInterrupt
    #         break
    #     sleep(config.loop_sleep)

    # # color sign => parking area
    # motion.forward_motor()
    # sleep(config.elapsed_k * elapsed + config.elapsed_b)
    # motion.stop_motor()
    # if dir == -1:
    #     motion.turn_left_motor()
    # else:
    #     motion.turn_right_motor()
    # motion.forward_motor()
    # sleep(config.park_time)

    # done
    # motion.stop_motor()

except KeyboardInterrupt:
    GPIO.cleanup()
    print("GPIO Good to Go")
    # save the history to txt files
    with open("front_dist_history.txt", "w") as f:
        for item in front_dist_history:
            f.write(str(item["dist"]) + " " + str(item["time"]) + "\n")
    with open("side_dist_history.txt", "w") as f:
        for item in side_dist_history:
            f.write(str(item["dist"]) + " " + str(item["time"]) + "\n")
    # move_end = time()
    # print("Time elapsed: ", move_end - move_start)

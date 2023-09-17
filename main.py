from PIL import Image
import  pyautogui
import pygetwindow 
import pydirectinput

from time import sleep
from time import time



def in_rgb_range(pixel: tuple, button_pixel: tuple) -> bool:
    res = 0
    for px, b_px in zip(pixel, button_pixel):
        if px in range(b_px-30, b_px+30):
            res += 1
    
    return res == 3


def in_rgb_range_fast(pixel: tuple, button_pixel: tuple) -> bool:
    res = 0
    for px, b_px in zip(pixel[:2], button_pixel[:2]):
        if b_px - 10 < px < b_px + 10:
            res += 1
    
    return res == 2


def need_to_play_game(image: Image, NIGHT_TIME_RGB = (94, 113, 128),
                       DAY_TIME_RGB = (248, 245, 167), 
                       RAINY_DAY_RGB = (248, 168, 109), 
                       CLOUDY_NIGHT_RGB = (115, 118, 110),
                       CLOUDY_DAY_RGB = (210, 133, 87)) -> bool:
    """
    Checks whatever we already need to play a game;
    If sign is showed, means that it's time
    """
    correct_number = 0
    for pixel in image.getdata():
        if correct_number > 5:
            return True
        if in_rgb_range(pixel, NIGHT_TIME_RGB) or in_rgb_range(pixel, DAY_TIME_RGB) \
            or in_rgb_range(pixel, RAINY_DAY_RGB) or in_rgb_range(pixel, CLOUDY_NIGHT_RGB)\
                or in_rgb_range(pixel, CLOUDY_DAY_RGB):
            correct_number += 1
    return False


def play_game_logic(image: Image, 
                    BUTTON_HIT_RGB = (174, 49, 209),
                    BUTTON_DOWN_RGB = (52, 145, 247),
                    BUTTON_LEFT_RGB = (246, 198, 67),
                    BUTTON_UP_RGB = (225, 50, 50), 
                    BUTTON_RIGHT_RGB = (45, 234, 43)
                    ):
    """
    Actual mini-game logic, here we need
    to process 5 different events:
    WASD + mouse tap;
    """
    
    img_colors = image.getcolors()

    if img_colors:
        for _, pixel in img_colors:
        
            if in_rgb_range_fast(pixel, BUTTON_RIGHT_RGB):
                pydirectinput.press("d")
                return
            elif in_rgb_range_fast(pixel, BUTTON_UP_RGB):
                pydirectinput.press("w")
                return
            elif in_rgb_range_fast(pixel, BUTTON_LEFT_RGB):
                pydirectinput.press("a")
                return
            elif in_rgb_range_fast(pixel, BUTTON_DOWN_RGB):
                pydirectinput.press("s")
                return
            elif in_rgb_range_fast(pixel, BUTTON_HIT_RGB):
                pydirectinput.press("space")
                return

    return False


def check_game_process(image: Image, WHITE_CLR_RGB = (251, 251, 251)):
    for pixel in image.getdata():
        if in_rgb_range_fast(pixel, WHITE_CLR_RGB):
            return True
    return False

def restart_minigame_process():
    print("[!] Sleeping for 3 secs..")
    sleep(3)
    pydirectinput.press("space")
    sleep(3)
    pydirectinput.press("space")
    return

window_name = "HoloCure"


w = pygetwindow.getWindowsWithTitle(window_name)[0]
w.activate()
sleep(1)


GAME_TRIGGER = False

while True:
    if not GAME_TRIGGER:
        frame = pyautogui.screenshot(region=(1220, 333, 100, 250))
        if need_to_play_game(frame):
            print("[+] Need to play game!")
            GAME_TRIGGER = True
            FIRST_WAIT = True
            PLAY_GAME_FALSE_COUNTS = 0
    else:

        frame = pyautogui.screenshot(region=(1530, 970, 40, 40))

        if play_game_logic(frame) == False:
            PLAY_GAME_FALSE_COUNTS += 1
        

        if FIRST_WAIT:
            while True:
                framePixel = pyautogui.screenshot(region=(1569, 925, 5, 5))
                if not check_game_process(framePixel):
                    print("[-] Waiting to pixel appear...")
                    sleep(0.1)
                    continue
                else:
                    print("[+] Pixel appeared, game started!") 
                    FIRST_WAIT = False
                    break

        if PLAY_GAME_FALSE_COUNTS > 50:
            framePixel = pyautogui.screenshot(region=(1569, 925, 5, 5))

            if not check_game_process(framePixel):
                print("[+] Mini-game Paused")
                GAME_TRIGGER = False
                restart_minigame_process()
                continue
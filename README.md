
# legendary-fishstick

As far as you know there is a game named [HoloCure](https://store.steampowered.com/app/2420510/HoloCure__Save_the_Fans/) 
and I am not very good at games and quite lazy, that's why this **POC** exists.  
This script will help you obtain millions of local currency, named `HoloCoins` with the help of **phishing** of course! 
This script uses some automatic trics with the help of `pyautogui`/`pydirectinput`/`PIL`.  


## Installation

Installation is quite easy, but setup is quite tricky.
To install, you can use `git`:

```bash
    $ git clone https://github.com/rive-n/legendary-fishstick.git && cd ./legendary-fishstick && python3 -m venv venv && source venv/bin/activate && pip3 install -r requirements.txt
```
    
## Usage/Examples

```bash
    $ python3 main.py
    ...
    [+] Pixel appeared, game started!
[+] Mini-game Paused
[!] Sleeping for 3 secs..
[+] Need to play game!
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[+] Pixel appeared, game started!
[+] Mini-game Paused
[!] Sleeping for 3 secs..
[+] Need to play game!
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[+] Pixel appeared, game started!
[+] Mini-game Paused
[!] Sleeping for 3 secs..
[+] Need to play game!
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[-] Waiting to pixel appear...
[+] Pixel appeared, game started!
...
```


## Features

- Allows you to get x4 speed at this mini-game and get **max** ~50 phishing combo;
- Full automatization;
- Auto-screen switching;
- Cross platform (?).


## Run Locally

Clone the project

```bash
   $ git clone https://github.com/rive-n/legendary-fishstick.git
```

Go to the project directory

```bash
   $ cd ./legendary-fishstick
```

Create `venv` and Install dependencies

```bash
  python3 -m venv venv && source venv/bin/activate && pip3 install -r requirements.txt
```

Start the application?

```bash
  python3 main.py
```

Not really. Now you need to get **YOUR** local (x,y) coordinates. I used for this `MPos`. Which coordinates you should ask? 

First of all, there is a pixel that allows you to block your character from moving, like showed below:

![image](https://github.com/rive-n/legendary-fishstick/assets/45512613/ec33b660-7e1b-4279-ac17-75d1e392610a)

After that, you have to trigger the mini-game start (using the `space` button, for instance) and get the location of the red circle:

![image](https://github.com/rive-n/legendary-fishstick/assets/45512613/faa77cc5-7a78-494b-9d72-b5082ad751fd)

After that, you should calculate the top-left location and add width/height for another sides in the next format:

`>>> im = pyautogui.screenshot(region=(x,y, width, height))`

Insert your tuple here:

```python
 if not GAME_TRIGGER:
        frame = pyautogui.screenshot(region=(1220, 333, 100, 250)) <--
```

After that, you need to do something similar with the actual mini-game bar:

![image](https://github.com/rive-n/legendary-fishstick/assets/45512613/a591ddc6-9536-448e-84c0-21873d83ee09)

And insert your data into the next code:

```
    else:

        frame = pyautogui.screenshot(region=(1530, 970, 40, 40))

        if play_game_logic(frame) == False:
            PLAY_GAME_FALSE_COUNTS += 1
```

And, of course, script should understand when the game process starts; To do this you need to calculate **OTHER** coords.. 

![image](https://github.com/rive-n/legendary-fishstick/assets/45512613/35626c47-ffc5-4868-9e30-63e2e3e2a488)

And insert this tuple to the next code snippet:

```python
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
```

## How does this works?

Well, it's not really hard to be honest. But I found some troubles while coding it. These troubles were connected with the different types of `RGB` events. 
That's why I used the next function to get more accurate information about the events:

```python3
def in_rgb_range(pixel: tuple, button_pixel: tuple) -> bool:
    res = 0
    for px, b_px in zip(pixel, button_pixel):
        if px in range(b_px-30, b_px+30):
            res += 1
    
    return res == 3
```

First of all, we need to somehow check if we really need to play the mini-game, and that's how:

```python
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
```

Here we check if the exclamation mark was created by clicking `space` bar. 

And after there is some logic which helps us to know if the mini-game is ended and we need to restart it:

```python
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
```

`if not check_game_process(framePixel)` checks for the white pixel which will appear only after the game is started!


## FAQ

#### Why? 

Why not?

#### Do I really need this?

Yes, you definitely do.


## Feedback

If you have any feedback, please reach out to me at [rive_n](https://t.me/rive_n)


## License

[MIT](https://choosealicense.com/licenses/mit/)


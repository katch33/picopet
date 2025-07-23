'''
Digital Pocket Pet

A Button - Info page with Hunger, Energy, Fun and Age (DONE)
B Button - Feed (DONE)
X Button - Sleep (DONE)
Y Button - Play (+10 Fun)

Main Screen To Do
- BG Art
- Cute animations/based on stats?
- Check for moving left or right and change sprites

DONE
- info page DONE
- eating animation DONE
- sleeping animation DONE

USEFUL TOOLS
display.line(x1, y1, x2, y2)
display.circle(x, y, r)
display.rectangle(x, y, w, h)
display.triangle(x1, y1, x2, y2, x3, y3)

display.polygon([
  (0, 10),
  (20, 10),
  (20, 0),
  (30, 20),
  (20, 30),
  (20, 20),
  (0, 20),
])

display.pixel(x, y)

display.text(text, x, y, wordwrap, scale, angle, spacing)

'''
# Imported Modules
import time
from machine import Pin
from time import sleep
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_RGB332
from pimoroni import Button, RGBLED
import random
import math

#used for the neopixel
led = RGBLED(6, 7, 8)

# button setup
A = Pin(12, Pin.IN, Pin.PULL_UP)
B = Pin(13, Pin.IN, Pin.PULL_UP)
X = Pin(14, Pin.IN, Pin.PULL_UP)
Y = Pin(15, Pin.IN, Pin.PULL_UP)
def callbacka(A):
    global interrupt_flag
    interrupt_flag = 1
def callbackb(B):
    global interrupt_flag
    interrupt_flag = 2
def callbackx(X):
    global interrupt_flag
    interrupt_flag = 3
def callbacky(Y):
    global interrupt_flag
    interrupt_flag = 4
    
A.irq(trigger=Pin.IRQ_FALLING, handler=callbacka)
B.irq(trigger=Pin.IRQ_FALLING, handler=callbackb)
X.irq(trigger=Pin.IRQ_FALLING, handler=callbackx)
Y.irq(trigger=Pin.IRQ_FALLING, handler=callbacky)
# initialises the interrupt flag to 0
interrupt_flag = 0

display = PicoGraphics(display = DISPLAY_PICO_DISPLAY, rotate = 45, pen_type=PEN_RGB332)

# set up constants for drawing
WIDTH, HEIGHT = display.get_bounds()

# create pen colours as RGB values
BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)
RED = display.create_pen(255, 0, 0)
YELLOW = display.create_pen(255, 255, 0)
GREEN = display.create_pen(0, 255, 0)
BLUE = display.create_pen(0, 0, 255)
CYAN = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)
ORANGE = display.create_pen(255, 95, 21)

display.set_font("bitmap8")
display.load_spritesheet("pet.rgb332")

SPRITE_XMAX = 15
SPRITE_YMAX = 15

# CUSTOM FUNCTIONS
# clear the screen to the selected colour
def clear(col):
    display.set_pen(col)
    display.clear()

# blink the LED on for the specified amount of time
def blink(r, g, b, delay):
    led.set_rgb(r, g, b)
    sleep(delay)
    led.set_rgb(0, 0, 0)
    
def lite(r, g, b):
    led.set_rgb(r, g, b)
    
def animate(o):
    o["frame"] += o["animspd"]
    if o["frame"] >= len(o["animx"]):
        o["frame"] = 0
    round_frame=math.floor(o["frame"])
    o["sprt"] = o["animx"][round_frame]

# display.set_backlight(x) where x= 0.0 - 1.0
brightness = 1.0
display.set_backlight(brightness)
lite(0, 0, 0) #turn neopixel off

#update interval for terminal debug info
dbg_time = 10
debug = False

# Global Variables and timers
t = 0

btn_time = 5
btn_delay = 5 # cooldown between button presses

walk_timer = 60 #countdown until check if walking
perform_time = 60 #countdown until check if performing

anims = {
    "walking": [0,1,2,3],
    "eating": [0,1],
    "sleeping": [0,1],
    "playing": [0,1,1,2,2,3,3,4,4,4,3,2,1,0,0]
    }

pet = {
    "x": 100,
    "y": 40,
    "tx": random.randint(10,220),
    "ty": random.randint(10,100),
    "spd": 50, #random.randint(10,15),
    
    "hunger": 50, #random.randint(80,100),
    "energy": 50, #random.randint(70,100),
    "fun": 50,
    "age": 0,
    
    "scale": 4,
    
    "walking": True,
    "sleeping": False,
    "eating": False,
    "playing": False,
    
    "animx": anims["walking"],
    "animy": 0,
    "animspd": 0.6,
    "frame": 0,
    "sprt": 0
    }


# setup before main loop
mode = "main"

clear(BLACK)

while True:
    
    print("T: " + str(t))
    
    t += 0.25
    if t > 10000:
        pet["age"] += 1
        t=0
    
    # Things that always happen
    animate(pet)
    
    btn_time -=1
    if btn_time < 0:
        btn_time = -1
    
    # These stats are always changing no matter what screeen you are on
    # age += 0.00001
    pet["hunger"] -= 0.001
    pet["energy"] -= 0.001
    pet["fun"] -= 0.001
    
    # Update loop for main screen
    if mode == "main":
        pet["animx"] = anims["walking"]
        pet["animy"] = 0
        # UPDATES THAT SHOULD ONLY HAPPEN ON THE MAIN SCREEN SHOULD GO HERE
        
        # decide if walking
        walk_timer -= 1
        if walk_timer < 0:
            pet["walking"] = random.choice([True, False])
            walk_timer = 60
        
        if pet["walking"] == True:
            # update pet position and use energy
            pet["x"] += int((pet["tx"] - pet["x"])/pet["spd"])
            pet["y"] += int((pet["ty"] - pet["y"])/pet["spd"])
            pet["hunger"] -= 0.005
            pet["energy"] -= 0.01
            pet["fun"] -= 0.001
            # choose new move target if close enough
            if abs(pet["x"] - pet["tx"])<pet["spd"]:
                pet["tx"] = random.randint(40,170)
            if abs(pet["y"] - pet["ty"])<pet["spd"]:
                pet["ty"] = random.randint(10,100)
        """       
        else:
            perform = random.choice([True, False])
            
            if perform == True:
                perform_time -= 1
                # CODE TO ANIMATE SMALL CUTE THINGS
                pet_sprt_y = 4
                pet_sprt_x += 1
                if pet_sprt_x > 8: 
                    pet_sprt_x = 0
                
                if perform_time < 0:
                    perform = False
        """
        
        # button checks for main screen
        if btn_time < 0:
            if interrupt_flag is 1: #A
                mode = "info"
                pet["x"] = 130
                pet["y"] = 50
                pet["scale"] = 10
                interrupt_flag = 0
                btn_time = btn_delay
            
            if interrupt_flag is 2: #B
                if pet["hunger"] < 90:
                    mode = "eating"
                    pet["x"] = 20
                    pet["y"] = 30
                    pet["scale"] = 10
                    interrupt_flag = 0
                    btn_time = btn_delay
                else:
                    mode = "main"
            
            if interrupt_flag is 3: #X
                if pet["energy"] < 90:
                    mode = "sleeping"
                    pet["x"] = 100
                    pet["y"] = 40
                    pet["scale"] = 10
                    interrupt_flag = 0
                    btn_time = btn_delay
            
            if interrupt_flag is 4: #Y
                if pet["fun"] < 90:
                    pet["fun"] += 10
                    mode = "main"
                    #pet_sprt_x = 0
                    #pet_sprt_y = 0
                    #pet["x"] = 130
                    #pet["y"] = 50
                    #pet["scale"] = 10
                    interrupt_flag = 0
                    btn_time = btn_delay
        else:
            interrupt_flag = 0
    
    elif mode == "info":
        pet["walking"] = False
        display.set_backlight(brightness)
        # incrememnt sprite
        pet["animx"] = anims["walking"]
        pet["animy"] = 0
            
        if btn_time < 0:
            if interrupt_flag is 1: #A
                pet["scale"] = 5
                mode = "main"
                interrupt_flag = 0
                btn_time = btn_delay
            if interrupt_flag is 2: #B
                pet["scale"] = 5
                mode = "main"
                interrupt_flag = 0
                btn_time = btn_delay
            if interrupt_flag is 3: #X
                if brightness < 1:
                    brightness += 0.25
                    print(brightness)
                interrupt_flag = 0
                btn_time = btn_delay
            if interrupt_flag is 4: #Y
                if brightness > 0.25:
                    brightness -= 0.25
                    print(brightness)
                interrupt_flag = 0
                btn_time = btn_delay
        else:
            interrupt_flag = 0
    
    elif mode == "eating":
        pet["walking"] = False
        if pet["hunger"] < 99:
            pet["animx"] = anims["eating"]
            pet["animy"] = 3
            pet["hunger"] += 1
        else:
            walking = True
            pet["scale"] = 5
            mode = "main"
    
    elif mode == "sleeping":
        pet["walking"] = False
        if pet["energy"] < 99:
            pet["animx"] = anims["sleeping"]
            pet["animy"] = 2
            pet["energy"] += 1
        else:
            pet["scale"] = 5
            mode = "main"
            
    elif mode == "fun":
        print("FUN")
        mode = "main"
                
    # DRAW CODE
    # clear the screen to black
    clear(BLACK)
    
    #display.sprite(spritesheet_x (0-15), spritesheet_y (0-15), x, y, scale, RGB332transparent_color ) 
    # eg. there are 16 8x8 sprites per 128 lines across, 0 to 15, and 16 down 0 to 15.
    display.sprite(round(pet["sprt"]), pet["animy"], pet["x"], pet["y"], pet["scale"], BLACK)
    
    if mode == "main":
        #info on button A
        display.set_pen(RED)
        display.rectangle(8, 8, 40, 40)
        
        display.set_pen(BLACK)
        display.rectangle(10, 10, 36, 36)
        
        display.set_pen(CYAN)
        display.text("in", 18, 13, scale = 2)
        display.text("fo", 18, 30, scale = 2)
        # food on button B
        display.set_pen(MAGENTA)
        display.circle(10+12 ,100+5, 18)
        display.sprite(11, 0, 10, 95, 3, BLACK)
        # bed on button X
        display.set_pen(BLUE)
        display.circle(190+24, 5+25, 18)
        display.sprite(12, 0, 197, 7, 4, BLACK)
        # fun on button Y
        display.set_pen(RED)
        display.circle(190+24, 5+100, 18)
        display.sprite(12, 1, 204, 95, 3, BLACK)
    
    if mode == "info":
        display.set_pen(CYAN)
        display.text("Hunger: " + str(round(pet["hunger"])), 10, 10, scale = 3)
        display.set_pen(ORANGE)
        display.text("Energy: " + str(round(pet["energy"])), 10, 45, scale = 3)
        display.set_pen(GREEN)
        display.text("Fun: " + str(round(pet["fun"])), 10, 80, scale = 3)
        display.set_pen(WHITE)
        display.text("Age: " + str(round(pet["age"])), 10, 110, scale = 3)
        display.set_pen(YELLOW)
        display.text("+", 220, 8, scale = 5)
        # PUT A SPRITE FOR BRIGHTNESS HERE
        display.text("-", 220, 80, scale = 5)
        display.text(str(brightness), 200, 50, scale = 2)
        
    if mode == "eating":
        #shows the noodles which are spread over 4 sprites
        display.sprite(13, 0, 140, 40, 5, BLACK)
        display.sprite(14, 0, 180, 40, 5, BLACK)
        display.sprite(13, 1, 140, 80, 5, BLACK)
        display.sprite(14, 1, 180, 80, 5, BLACK)
    
    if mode == "sleeping":
        display.sprite(10, 0, pet["x"] + 10, pet["y"] - 20, 5, BLACK)
    
    #update screen
    display.update()
    
    # DEBUG CODE
    # debug current sprite to terminal output
    if debug == True:
        dbg_time -= 1
        if dbg_time < 0:
            print("Position:" + str(pet["x"]) + "/" + str(pet["y"]))
            print("Target:" + str(pet["tx"]) + "/" + str(pet["ty"]))
            print("Hunger:" + str(pet["hunger"]))
            print("Energy:" + str(pet["x"]) + "/" + str(pet["y"]))
            print("Walking:" + str(pet["x"]) + "/" + str(pet["y"]))
            print("Age:" + str(pet["x"]) + "/" + str(pet["y"]))
            dbg_time = 10
            
    # interval - 0.1 is planned value
    time.sleep(0.1)



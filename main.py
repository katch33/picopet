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
    
# lock number to range
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

# blink the LED on for the specified amount of time
def blink(r, g, b, delay):
    led.set_rgb(r, g, b)
    sleep(delay)
    led.set_rgb(0, 0, 0)
    
def lite(r, g, b):
    led.set_rgb(r, g, b)

# display.set_backlight(x) where x= 0.0 - 1.0
brightness = 1.0
display.set_backlight(brightness)
lite(0, 0, 0) #turn neopixel off

# TIMERS
btn_time = 0
btn_delay = 5 # cooldown for button presses

walk_timer = 60
perform_time = 60

#update interval for terminal debug info
dbg_time = 10
debug = False

# PET CODE
#starting sprite
pet_sprt_x = 0
pet_sprt_y = 0

#randomise initial target
tx = random.randint(10,220)
ty = random.randint(10,100)
#how fast to move there
spd = random.randint(10,15)
#where to begin
x = 100 #init x pos
y = 40 #init y pos

#starting stats
hunger = random.randint(80,100)
energy = random.randint(70,100)
fun = 60
age = 0

pet_scale = 4 # draw scale
walking = True

# setup before main loop
mode = "main"

clear(BLACK)

t = 0

while True:
    t += 0.25
    if t > 10000:
        age += 1
        t=0
    
    # Things that always happen
    btn_time -=1
    if btn_time < 0:
        btn_time = -1
    
    # These stats are always changing no matter what screeen you are on
    # age += 0.00001
    hunger -= 0.001
    energy -= 0.001
    fun -= 0.001
    
    # Update loop for main screen
    if mode == "main":
        # UPDATES THAT SHOULD ONLY HAPPEN ON THE MAIN SCREEN SHOULD GO HERE
        
        # decide if walking
        walk_timer -= 1
        if walk_timer < 0:
            walking = random.choice([True, False])
            walk_timer = 60
        
        if walking == True:
            # update pet position and use energy
            x += int((tx - x)/spd)
            y += int((ty - y)/spd)
            energy -= 0.01
            hunger -= 0.005
            fun -= 0.01
            # choose new move target if close enough
            if abs(x - tx)<spd:
                tx = random.randint(10,220)
            if abs(y - ty)<spd:
                ty = random.randint(10,100)
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

        # DEBUG INFO ###
        #time.sleep(2)
        #print("Frame: " + str(pet_sprt_x))
        #time.sleep(2)
        ################
        pet_sprt_x += 0.40
        if pet_sprt_x > 3: 
            pet_sprt_x = 0
        
        # button checks for main screen
        if btn_time < 0:
            if interrupt_flag is 1: #A
                mode = "info"
                pet_sprt_x = 0
                pet_sprt_y = 0
                x = 130
                y = 50
                pet_scale = 10
                interrupt_flag = 0
                btn_time = btn_delay
            
            if interrupt_flag is 2: #B
                if hunger < 90:
                    mode = "eating"
                    pet_sprt_x = 0
                    pet_sprt_y = 3
                    x = 20
                    y = 30
                    pet_scale = 10
                    interrupt_flag = 0
                    btn_time = btn_delay
                else:
                    mode = "main"
            
            if interrupt_flag is 3: #X
                if energy < 90:
                    mode = "sleeping"
                    pet_sprt_x = 0
                    pet_sprt_y = 2
                    x = 100
                    y = 40
                    pet_scale = 10
                    interrupt_flag = 0
                    btn_time = btn_delay
            
            if interrupt_flag is 4: #Y
                if fun < 90:
                    fun += 10
                    mode = "main"
                    #pet_sprt_x = 0
                    #pet_sprt_y = 0
                    #x = 130
                    #y = 50
                    #pet_scale = 10
                    interrupt_flag = 0
                    btn_time = btn_delay
        else:
            interrupt_flag = 0
    
    elif mode == "info":
        walking = False
        display.set_backlight(brightness)
        # incrememnt sprite
        pet_sprt_x += 0.2
        if pet_sprt_x > 1: 
            pet_sprt_x = 0
            
        if btn_time < 0:
            if interrupt_flag is 1: #A
                pet_scale = 5
                mode = "main"
                interrupt_flag = 0
                btn_time = btn_delay
            if interrupt_flag is 2: #B
                pet_scale = 5
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
        walking = False
        pet_sprt_y = 3
        if hunger < 99:
            pet_sprt_x += 0.15
            if pet_sprt_x > 1:
                pet_sprt_x = 0
            hunger += 1
        else:
            walking = True
            pet_sprt_x = 0
            pet_sprt_y = 0
            pet_scale = 5
            mode = "main"
    
    elif mode == "sleeping":
        walking = False
        pet_sprt_y = 2
        if energy < 99:
            pet_sprt_x += 0.05
            if pet_sprt_x > 1:
                pet_sprt_x = 0
            energy += 0.1
        else:
            pet_sprt_x = 0
            pet_sprt_y = 0
            pet_scale = 5
            mode = "main"
            
    elif mode == "fun":
        print("FUN")
        mode = "main"
                
    # DRAW CODE
    # clear the screen to black
    clear(BLACK)
    
    if mode == "main":
        #info on button A
        display.set_pen(CYAN)
        display.text("info", 10, 15, scale = 3)
        # food on button B
        display.set_pen(MAGENTA)
        display.circle(10+12,100+10,18)
        display.sprite(11, 0, 10, 100, 3, BLACK)
        # bed on button X
        display.set_pen(BLUE)
        display.circle(190+21,5+25,22)
        display.sprite(12, 0, 190, 5, 5, BLACK)
        # fun on button Y
        display.set_pen(WHITE)
        display.text("fun +10", 150, 100, scale = 3)
        #display.sprite(?, 0, 190, 100, 3, BLACK)
    
    if mode == "info":
        display.set_pen(CYAN)
        display.text("Hunger: " + str(round(hunger)), 10, 10, scale = 3)
        display.set_pen(ORANGE)
        display.text("Energy: " + str(round(energy)), 10, 45, scale = 3)
        display.set_pen(GREEN)
        display.text("Fun: " + str(round(fun)), 10, 80, scale = 3)
        display.set_pen(WHITE)
        display.text("Age: " + str(round(age)), 10, 110, scale = 3)
        display.set_pen(YELLOW)
        display.text("+", 220, 8, scale = 5)
        display.text("-", 220, 80, scale = 5)
        display.text(str(brightness), 200, 50, scale = 2)
        
    if mode == "eating":
        #shows the noodles which are spread over 4 sprites
        display.sprite(13, 0, 140, 40, 5, BLACK)
        display.sprite(14, 0, 180, 40, 5, BLACK)
        display.sprite(13, 1, 140, 80, 5, BLACK)
        display.sprite(14, 1, 180, 80, 5, BLACK)
    
    if mode == "sleeping":
        display.sprite(10, 0, x+10, y-20, 5, BLACK)
    
    #display.sprite(spritesheet_x (0-15), spritesheet_y (0-15), x, y, scale, RGB332transparent_color ) 
    # eg. there are 16 8x8 sprites per 128 lines across, 0 to 15, and 16 down 0 to 15.
    display.sprite(round(pet_sprt_x), pet_sprt_y, x, y, pet_scale, BLACK)
    
    #update screen
    display.update()
    
    # DEBUG CODE
    # debug current sprite to terminal output
    if debug == True:
        dbg_time -= 1
        if dbg_time < 0:
            print("Position:" + str(x) + "/" + str(y))
            print("Target:" + str(tx) + "/" + str(ty))
            print("Hunger:" + str(hunger))
            print("Energy:" + str(energy))
            print("Walking:" + str(walking))
            print("Age:" + str(age))
            print("T: " + str(t))
            dbg_time = 10
            
    # interval - 0.1 is planned value
    time.sleep(0.1)

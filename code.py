"""CircuitPython PyPortal Green/Blue Neopixel Ring control"""
import time
import board
from adafruit_pyportal import PyPortal
from adafruit_button import Button
import neopixel
from adafruit_bitmap_font import bitmap_font
from adafruit_progressbar import ProgressBar

GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
# Set the background color
BACKGROUND_COLOR = 0x443355

screen_width = 320 # Adjust to fit your device
screen_height = 240 # Adjust to fit your device
 
# We want two big buttons at the bottom of the screen
BUTTON_HEIGHT = int(screen_height/3.2)
BUTTON_WIDTH = int(screen_width/3)
BOTTOM_BUTTON_Y = int(screen_height-BUTTON_HEIGHT)

 # Set the NeoPixel brightness
BRIGHTNESS = 0.1

BAR_WIDTH = screen_width - 40
BAR_HEIGHT = screen_height - (3 * BUTTON_HEIGHT)

BARX = screen_width // 2 - BAR_WIDTH // 2
BARY = BUTTON_HEIGHT 

progress_bar = ProgressBar(
    BARX, BARY, BAR_WIDTH, BAR_HEIGHT, 1.0, bar_color=0x666666, outline_color=0xFFFFFF
)

# Setup PyPortal without networking
pyportal = PyPortal(default_bg=BACKGROUND_COLOR)

num_pixels = 16 # Adjust to fit your device
ring_1 = neopixel.NeoPixel(board.D4, num_pixels, brightness=BRIGHTNESS) # Adjust to fit your device
ring_1.fill(GREEN)
ring_1.show()

buttons = []
font = bitmap_font.load_font("/fonts/Arial-ItalicMT-17.bdf")
font.load_glyphs(b'abcdefghjiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890- ()')

# Main User Interface Buttons
button_brighter = Button(x=0, y=0,
                      width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                      label="<", label_font=font, label_color=0xff7e00,
                      fill_color=0x5c5b5c, outline_color=0x767676,
                      selected_fill=0x1a1a1a, selected_outline=0x2e2e2e,
                      selected_label=0x525252)
buttons.append(button_brighter)  # adding this button to the buttons group
 
button_dimmer = Button(x=BUTTON_WIDTH, y=0,
                      width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                      label=">", label_font=font, label_color=0xff7e00,
                      fill_color=0x5c5b5c, outline_color=0x767676,
                      selected_fill=0x1a1a1a, selected_outline=0x2e2e2e,
                      selected_label=0x525252)
buttons.append(button_dimmer)  # adding this button to the buttons group
 
button_reset = Button(x=BUTTON_WIDTH*2, y=0,
                      width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                      label="Reset", label_font=font, label_color=0xff7e00,
                      fill_color=0x5c5b5c, outline_color=0x767676,
                      selected_fill=0x1a1a1a, selected_outline=0x2e2e2e,
                      selected_label=0x525252)
buttons.append(button_reset)  # adding this button to the buttons group
 
button_off = Button(x=0, y=BOTTOM_BUTTON_Y-BUTTON_HEIGHT,
                       width=screen_width, height=BUTTON_HEIGHT,
                       label="Off", label_font=font, label_color=0xff7e00,
                       fill_color=0x5c5b5c, outline_color=0x767676,
                       selected_fill=0x1a1a1a, selected_outline=0x2e2e2e,
                       selected_label=0x525252)
buttons.append(button_off)  # adding this button to the buttons group

button_green = Button(x=0, y=BOTTOM_BUTTON_Y,
                width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                style=Button.SHADOWROUNDRECT,
                selected_outline=0xff0000, selected_fill=0x66ff66,
                fill_color=GREEN, outline_color=0x222222)
buttons.append(button_green)  # adding this button to the buttons group
 
button_blue = Button(x=BUTTON_WIDTH, y=BOTTOM_BUTTON_Y,
                width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                style=Button.SHADOWROUNDRECT,
                selected_outline=0xff0000, selected_fill=0x0080ff,
                fill_color=BLUE, outline_color=0x222222)
buttons.append(button_blue)  # adding this button to the buttons group

button_white = Button(x=BUTTON_WIDTH*2, y=BOTTOM_BUTTON_Y,
                width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                style=Button.SHADOWROUNDRECT,
                selected_outline=0xff0000, selected_fill=0xa0a0a0,
                fill_color=WHITE, outline_color=0x222222)
buttons.append(button_white)  # adding this button to the buttons group

# Add all of the main buttons to the splash Group
for b in buttons:
    pyportal.splash.append(b.group)

# Append progress_bar to the splash group
pyportal.splash.append(progress_bar)
progress_bar.progress = BRIGHTNESS

while True:
    touch = pyportal.touchscreen.touch_point
    if touch:
        for i,button in enumerate(buttons):
            if button.contains(touch):
                print('button%d pressed' % i)
                if i == 0 and BRIGHTNESS > 0.01 and ON:
                    BRIGHTNESS = BRIGHTNESS - 0.01
                    ring_1.brightness = BRIGHTNESS
                    ring_1.show()
                if i == 1 and BRIGHTNESS <= 0.99 and ON:
                    BRIGHTNESS = BRIGHTNESS + 0.01
                    ring_1.brightness = BRIGHTNESS
                    ring_1.show()
                if i == 2 and ON:
                    BRIGHTNESS = 0.1
                    ring_1.brightness = BRIGHTNESS
                    ring_1.show()
                if i == 3:
                    ring_1.fill(BLACK)
                    ring_1.show()
                    button.selected = True
                    buttons[4].selected = False
                    buttons[5].selected = False
                    buttons[6].selected = False
                    BRIGHTNESS = 0.0
                    ON = False
                if i == 4:
                    ring_1.fill(GREEN)
                    ring_1.show()
                    button.selected = True
                    buttons[3].selected = False
                    buttons[5].selected = False
                    buttons[6].selected = False
                    BRIGHTNESS = ring_1.brightness
                    ON = True
                if i == 5:
                    ring_1.fill(BLUE)
                    ring_1.show()
                    button.selected = True
                    buttons[3].selected = False
                    buttons[4].selected = False
                    buttons[6].selected = False
                    BRIGHTNESS = ring_1.brightness
                    ON = True
                if i == 6:
                    ring_1.fill(WHITE)
                    ring_1.show()
                    button.selected = True
                    buttons[3].selected = False
                    buttons[4].selected = False
                    buttons[5].selected = False
                    BRIGHTNESS = ring_1.brightness
                    ON = True
                progress_bar.progress = BRIGHTNESS

    time.sleep(0.05)

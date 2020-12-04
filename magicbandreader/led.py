from enum import Enum

import board
import neopixel
import time

class LedColor(Enum):
    RED = (0,255,0)
    ELECTRIC_RED = (3,228,3)
    ORANGE = (255,165,0)
    DARK_ORANGE = (255,140,0)
    YELLOW = (255,255,0)
    CANARY_YELLOW = (255,237,0)
    GREEN = (255,0,0)
    LASALLE_GREEN = (0,128,38)
    BLUE = (0,0,255)
    PATRIARCH = (117,7,135)
    LIGHT_BLUE = (153,204,255)
    WHITE = (255,255,255)
    PURPLE = (0,153,153)
    GRAY = (128,128,128)
    STITCH = (0,39,144)

class LedController:
    def __init__(self, gpio_pin=board.D18, total_pixels=144, brightness=1.0, auto_write=False, pixel_order=neopixel.RGB):
        self.gpio_pin = gpio_pin
        self.total_pixels = total_pixels
        self.pixels = neopixel.NeoPixel(gpio_pin, total_pixels, brightness=brightness, auto_write=auto_write, pixel_order=pixel_order)
        self.startup_sequence()

    def startup_sequence(self):
        for color in LedColor:
            self.lights_on(color)
            time.sleep(.25)

        self.lights_off()

    def lights_on(self, led_color):
        for i in range(self.total_pixels):
            self.pixels[i] = led_color.value
        self.pixels.show()

    def lights_off(self):
        for i in range(self.total_pixels):
            self.pixels[i] = 0
        self.pixels.show()

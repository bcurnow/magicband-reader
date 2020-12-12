from enum import Enum
from functools import wraps

import board
import neopixel
import time


class LedColor(Enum):
    ALICE_BLUE = (240, 248, 255)
    ANTIQUE_WHITE = (250, 235, 215)
    AQUA = (0, 255, 255)
    AQUA_MARINE = (127, 255, 212)
    AZURE = (240, 255, 255)
    BEIGE = (245, 245, 220)
    BISQUE = (255, 228, 196)
    BLACK = (0, 0, 0)
    BLANCHED_ALMOND = (255, 235, 205)
    BLUE = (0, 0, 255)
    BLUE_VIOLET = (138, 43, 226)
    BROWN = (165, 42, 42)
    BURLY_WOOD = (222, 184, 135)
    CADET_BLUE = (95, 158, 160)
    CHARTREUSE = (127, 255, 0)
    CHOCOLATE = (210, 105, 30)
    CORAL = (255, 127, 80)
    CORN_FLOWER_BLUE = (100, 149, 237)
    CORN_SILK = (255, 248, 220)
    CRIMSON = (220, 20, 60)
    DARK_BLUE = (0, 0, 139)
    DARK_CYAN = (0, 139, 139)
    DARK_GOLDEN_ROD = (184, 134, 11)
    DARK_GRAY = (169, 169, 169)
    DARK_GREEN = (0, 100, 0)
    DARK_KHAKI = (189, 183, 107)
    DARK_MAGENTA = (139, 0, 139)
    DARK_OLIVE_GREEN = (85, 107, 47)
    DARK_ORANGE = (255, 140, 0)
    DARK_ORCHID = (153, 50, 204)
    DARK_RED = (139, 0, 0)
    DARK_SALMON = (233, 150, 122)
    DARK_SEA_GREEN = (143, 188, 143)
    DARK_SLATE_BLUE = (72, 61, 139)
    DARK_SLATE_GRAY = (47, 79, 79)
    DARK_TURQUOISE = (0, 206, 209)
    DARK_VIOLET = (148, 0, 211)
    DEEP_PINK = (255, 20, 147)
    DEEP_SKY_BLUE = (0, 191, 255)
    DIM_GRAY = (105, 105, 105)
    DODGER_BLUE = (30, 144, 255)
    FIREBRICK = (178, 34, 34)
    FLORAL_WHITE = (255, 250, 240)
    FOREST_GREEN = (34, 139, 34)
    GAINSBORO = (220, 220, 220)
    GHOST_WHITE = (248, 248, 255)
    GOLD = (255, 215, 0)
    GOLDEN_ROD = (218, 165, 32)
    GRAY = (128, 128, 128)
    GREEN = (0, 128, 0)
    GREEN_YELLOW = (173, 255, 47)
    HONEYDEW = (240, 255, 240)
    HOT_PINK = (255, 105, 180)
    INDIAN_RED = (205, 92, 92)
    INDIGO = (75, 0, 130)
    IVORY = (255, 255, 240)
    KHAKI = (240, 230, 140)
    LAVENDER = (230, 230, 250)
    LAVENDER_BLUSH = (255, 240, 245)
    LAWN_GREEN = (124, 252, 0)
    LEMON_CHIFFON = (255, 250, 205)
    LIGHT_BLUE = (173, 216, 230)
    LIGHT_CORAL = (240, 128, 128)
    LIGHT_CYAN = (224, 255, 255)
    LIGHT_GOLDEN_ROD_YELLOW = (250, 250, 210)
    LIGHT_GRAY = (211, 211, 211)
    LIGHT_GREEN = (144, 238, 144)
    LIGHT_PINK = (255, 182, 193)
    LIGHT_SALMON = (255, 160, 122)
    LIGHT_SEA_GREEN = (32, 178, 170)
    LIGHT_SKY_BLUE = (135, 206, 250)
    LIGHT_SLATE_GRAY = (119, 136, 153)
    LIGHT_STEEL_BLUE = (176, 196, 222)
    LIGHT_YELLOW = (255, 255, 224)
    LIME = (0, 255, 0)
    LIME_GREEN = (50, 205, 50)
    LINEN = (250, 240, 230)
    MAGENTA = (255, 0, 255)
    MAROON = (128, 0, 0)
    MEDIUM_AQUA_MARINE = (102, 205, 170)
    MEDIUM_BLUE = (0, 0, 205)
    MEDIUM_ORCHID = (186, 85, 211)
    MEDIUM_PURPLE = (147, 112, 219)
    MEDIUM_SEA_GREEN = (60, 179, 113)
    MEDIUM_SLATE_BLUE = (123, 104, 238)
    MEDIUM_SPRING_GREEN = (0, 250, 154)
    MEDIUM_TURQUOISE = (72, 209, 204)
    MEDIUM_VIOLET_RED = (199, 21, 133)
    MIDNIGHT_BLUE = (25, 25, 112)
    MINT_CREAM = (245, 255, 250)
    MISTY_ROSE = (255, 228, 225)
    MOCCASIN = (255, 228, 181)
    NAVAJO_WHITE = (255, 222, 173)
    NAVY = (0, 0, 128)
    OLD_LACE = (253, 245, 230)
    OLIVE = (128, 128, 0)
    OLIVE_DRAB = (107, 142, 35)
    ORANGE = (255, 165, 0)
    ORANGE_RED = (255, 69, 0)
    ORCHID = (218, 112, 214)
    PALE_GOLDEN_ROD = (238, 232, 170)
    PALE_GREEN = (152, 251, 152)
    PALE_TURQUOISE = (175, 238, 238)
    PALE_VIOLET_RED = (219, 112, 147)
    PAPAYA_WHIP = (255, 239, 213)
    PEACH_PUFF = (255, 218, 185)
    PERU = (205, 133, 63)
    PINK = (255, 192, 203)
    PLUM = (221, 160, 221)
    POWDER_BLUE = (176, 224, 230)
    PURPLE = (128, 0, 128)
    RED = (255, 0, 0)
    ROSY_BROWN = (188, 143, 143)
    ROYAL_BLUE = (65, 105, 225)
    SADDLE_BROWN = (139, 69, 19)
    SALMON = (250, 128, 114)
    SANDY_BROWN = (244, 164, 96)
    SEA_GREEN = (46, 139, 87)
    SEA_SHELL = (255, 245, 238)
    SIENNA = (160, 82, 45)
    SILVER = (192, 192, 192)
    SKY_BLUE = (135, 206, 235)
    SLATE_BLUE = (106, 90, 205)
    SLATE_GRAY = (112, 128, 144)
    SNOW = (255, 250, 250)
    SPRING_GREEN = (0, 255, 127)
    STEEL_BLUE = (70, 130, 180)
    TAN = (210, 180, 140)
    TEAL = (0, 128, 128)
    THISTLE = (216, 191, 216)
    TOMATO = (255, 99, 71)
    TURQUOISE = (64, 224, 208)
    VIOLET = (238, 130, 238)
    WHEAT = (245, 222, 179)
    WHITE = (255, 255, 255)
    WHITE_SMOKE = (245, 245, 245)
    YELLOW = (255, 255, 0)
    YELLOW_GREEN = (154, 205, 50)


class LedController:
    def __init__(self,
                 brightness=.5,
                 outer_pixels=40,
                 inner_pixels=15,
                 ):
        self.brightness = brightness
        self.outer_pixels = outer_pixels
        self.inner_pixels = inner_pixels
        self.pixels = neopixel.NeoPixel(
            board.D18,
            outer_pixels + inner_pixels,
            brightness=brightness,
            auto_write=False,
            pixel_order=neopixel.GRB
            )
        self.startup_sequence()

    def startup_sequence(self):
        """ Executes a specific pattern to provide a visual indicators that the controller is started."""
        self.blink(LedColor.WHITE, iterations=2, sleep_sec=.50)

    def blink(self, led_color, brightness=None, iterations=3, sleep_sec=.25):
        """ Implements a "blink" effect by turning on and off the lights."""
        self.pixels.brightness = self._brightness(brightness)
        for i in range(iterations):
            self.lights_on(led_color, brightness=self._brightness(brightness))
            time.sleep(sleep_sec)
            self.lights_off()
            # Skip the sleeping for the final iteration, no need to wait, the lights are already off
            if i < (iterations - 1):
                time.sleep(sleep_sec)

    def lights_on(self, led_color, brightness=None):
        """ Turns all the leds on to a specific color."""
        self.pixels.brightness = self._brightness(brightness)
        self.pixels.fill(led_color.value)
        self.pixels.show()

    def fade_on(self, color, brightness=None, sleep_sec=.01):
        """ Turns all the leds on to a specific color but raises the brightness gradually."""
        target_brightness = self._brightness(brightness)
        self.pixels.fill(color.value)

        for current_brightness in range(1, (int(target_brightness * 100)) + 1):
            self.pixels.brightness = current_brightness / 100
            self.pixels.show()
            time.sleep(sleep_sec)

    def lights_off(self):
        """ Turns all the leds off."""
        self.pixels.fill(0)
        self.pixels.show()

    def fade_off(self, brightness=None, sleep_sec=.01):
        """ Turns all the leds off but lowers the brightness grandually."""
        max_brightness = self._brightness(brightness)
        for current_brightness in reversed(range((int(max_brightness * 100)) + 1)):
            self.pixels.brightness = current_brightness / 100
            self.pixels.show()
            time.sleep(sleep_sec)
        # Make sure to turn all the LEDs back off otherwise they'll remember the color
        # they were and come back on with the next call to show()
        self.pixels.fill(0)

    def color_chase(self, color, brightness=None, sleep_sec=.1, reverse=False, effect_width=8):
        self.pixels.brightness = self._brightness(brightness)
        """ Creates a a moving set of leds, effect_width long, which move "around" the outer loop."""
        for i in range(self.outer_pixels + effect_width + 1):
            if i <= self.outer_pixels:
                on = i
                if reverse:
                    on = self.outer_pixels - on
                self.pixels[on] = color.value

            if i >= effect_width:
                off = i - (effect_width)
                if reverse:
                    off = self.outer_pixels - off
                self.pixels[off] = 0

            self.pixels.show()
            if i < self.outer_pixels + effect_width:
                time.sleep(sleep_sec)

    def spin(self, color, brightness=None, reverse=False, effect_width=8):
        self.color_chase(color, self._brightness(brightness), .01, reverse, effect_width)
        self.color_chase(color, self._brightness(brightness), .001, reverse, effect_width)
        self.color_chase(color, self._brightness(brightness), .0001, reverse, effect_width)
        self.color_chase(color, self._brightness(brightness), .0001, reverse, effect_width)


    def _brightness(self, brightness):
        if brightness:
            return brightness
        return self.brightness

import threading
import time

from magicbandreader.handlers import AbstractHandler
from magicbandreader.led import LedController, LedColor

class LightMickeyHandler(AbstractHandler):
    """ Responsible for lighting up the outer ring and innerr ring with appropriate colors based on authentication status."""
    def __init__(self, ctx):
        super().__init__(priority=3)
        self.ctx = ctx

    def handle_authorized_event(self, event):
        threading.Thread(
            target=self._light_mickey,
            args=(LedColor.GREEN,)
        ).start()

    def handle_unauthorized_event(self, event):
        threading.Thread(
            target=self._light_mickey,
            args=(LedColor.STEEL_BLUE,)
        ).start()

    def _light_mickey(self, color):
        self.ctx.led_controller.fade_on(color)
        time.sleep(1)
        self.ctx.led_controller.fade_off()

def register(ctx):
    return LightMickeyHandler(ctx)
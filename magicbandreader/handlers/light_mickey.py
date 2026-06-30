import threading

from magicbandreader.handlers import AbstractHandler
from magicbandreader.led import LedColor


class LightMickeyHandler(AbstractHandler):
    """Responsible for lighting up the outer ring and inner ring with appropriate colors based on authentication status."""

    def __init__(self, ctx):
        super().__init__(priority=30)
        self.ctx = ctx

    def handle_authorized_event(self, event):
        self.ctx.light_thread = threading.Thread(target=self.ctx.led_controller.fade_on, args=(LedColor.GREEN,))
        self.ctx.light_thread.start()

    def handle_unauthorized_event(self, event):
        self.ctx.light_thread = threading.Thread(target=self.ctx.led_controller.fade_on, args=(LedColor.BLUE,))
        self.ctx.light_thread.start()


def register(ctx):
    return LightMickeyHandler(ctx)

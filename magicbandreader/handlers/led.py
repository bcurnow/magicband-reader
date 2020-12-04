from magicbandreader.handlers import AbstractHandler
from magicbandreader.led import LedController

class LedHandler(AbstractHandler):
    def __init__(self, ctx):
        super().__init__(priority=1)
        self.led_control = LedController(brightness=.10)


    def handle_authorized_event(self, event):
        pass



def register(ctx):
    return LedHandler(ctx)

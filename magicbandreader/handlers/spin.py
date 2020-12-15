import threading

from magicbandreader.handlers import AbstractHandler
from magicbandreader.led import LedColor


class SpinHandler(AbstractHandler):
    """ Spins the lights around the main ring."""
    def __init__(self, ctx):
        super().__init__(priority=0)
        self.ctx = ctx

    def handle_event(self, event):
        """ Override the handle_event method from the super class as we haven't authorized yet."""
        t = threading.Thread(target=self._spin)
        self.ctx.spin_thread = t
        t.start()


    def _spin(self):
        self.ctx.led_controller.spin(LedColor.WHITE, reverse=True)


def register(ctx):
    return SpinHandler(ctx)

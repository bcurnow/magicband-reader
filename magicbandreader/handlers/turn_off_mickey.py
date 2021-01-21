from magicbandreader.handlers import AbstractHandler


class TurnOffMickeyHandler(AbstractHandler):
    """ Responsible for turning off the outer and inner rings"""
    def __init__(self, ctx):
        super().__init__(priority=50)
        self.ctx = ctx

    def handle_event(self, event):
        """ Override the handle_event method from the super class as we don't care about the event, just that we had one"""
        self.ctx.led_controller.fade_off()


def register(ctx):
    return TurnOffMickeyHandler(ctx)

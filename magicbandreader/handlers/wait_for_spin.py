import logging

from magicbandreader.handlers import AbstractHandler


class WaitForSpinHandler(AbstractHandler):
    """ Spins the lights around the main ring."""
    def __init__(self, ctx):
        super().__init__(priority=20)
        self.ctx = ctx

    def handle_event(self, event):
        """ Override the handle_event method from the super class as we don't care about the type."""
        if hasattr(self.ctx, 'spin_thread'):
            # Wait until the spinning is completed
            self.ctx.spin_thread.join()
        else:
            logging.warning('Unable to find spin_thread in context.')


def register(ctx):
    return WaitForSpinHandler(ctx)

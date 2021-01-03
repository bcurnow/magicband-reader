from magicbandreader.handlers import AbstractHandler
from magicbandreader.audio import load_sound, play_sound


class ReadSoundHandler(AbstractHandler):
    """ Plays a sound indicating a band was read."""
    def __init__(self, ctx):
        super().__init__(priority=0)
        self.read_sound = load_sound(ctx, ctx.read_sound)

    def handle_event(self, event):
        """ Override the handle_event method from the super class as we don't care about the event, just that we read data."""
        play_sound(self.read_sound)


def register(ctx):
    return ReadSoundHandler(ctx)

import os

# Don't print the support info to stdout upon startup
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from magicbandreader.handlers import AbstractHandler


class SoundHandler(AbstractHandler):
    def __init__(self, ctx):
        super().__init__(priority=99)
        pygame.mixer.init()
        self.sound_dir = os.path.join(os.path.dirname(__file__), '../sounds')
        self.default_sound = pygame.mixer.Sound(os.path.join(self.sound_dir, 'default.wav'))
        self.default_sound.set_volume(ctx.volume_level)


    def handle_authorized_event(self, event):
        self.default_sound.play()


def register(ctx):
    return SoundHandler(ctx)

import os

# Don't print the support info to stdout upon startup
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from magicbandreader.handlers import AbstractHandler


class AuthorizationSoundHandler(AbstractHandler):
    def __init__(self, ctx):
        super().__init__(priority=4)
        pygame.mixer.init()
        self.authorized_sound = pygame.mixer.Sound(os.path.join(ctx.sound_dir, ctx.authorized_sound))
        self.authorized_sound.set_volume(ctx.volume_level)
        self.unauthorized_sound = pygame.mixer.Sound(os.path.join(ctx.sound_dir, ctx.unauthorized_sound))
        self.unauthorized_sound.set_volume(ctx.volume_level)

    def handle_authorized_event(self, event):
        self.authorized_sound.play()

    def handle_unauthorized_event(self, event):
        self.unauthorized_sound.play()

def register(ctx):
    return AuthorizationSoundHandler(ctx)

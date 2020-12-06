from magicbandreader.handlers import AbstractHandler
from magicbandreader.audio import load_sound, play_sound


class AuthorizationSoundHandler(AbstractHandler):
    def __init__(self, ctx):
        super().__init__(priority=40)
        self.authorized_sound = load_sound(ctx, ctx.authorized_sound)
        self.unauthorized_sound = load_sound(ctx, ctx.unauthorized_sound)

    def handle_authorized_event(self, event):
        play_sound(self.authorized_sound)

    def handle_unauthorized_event(self, event):
        play_sound(self.unauthorized_sound)


def register(ctx):
    return AuthorizationSoundHandler(ctx)

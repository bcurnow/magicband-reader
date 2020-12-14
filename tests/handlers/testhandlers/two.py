from magicbandreader.handlers import AbstractHandler


class TwoHandler(AbstractHandler):
    pass


def register(ctx):
    return TwoHandler(priority=2)

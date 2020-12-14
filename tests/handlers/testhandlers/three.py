from magicbandreader.handlers import AbstractHandler


class ThreeHandler(AbstractHandler):
    pass


def register(ctx):
    return ThreeHandler(priority=1)

from magicbandreader.handlers import AbstractHandler


class OneHandler(AbstractHandler):
    pass


def register(ctx):
    return OneHandler(priority=3)

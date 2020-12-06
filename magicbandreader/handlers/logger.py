import logging

from magicbandreader.handlers import AbstractHandler


class LoggingHandler(AbstractHandler):
    def __init__(self, ctx):
        super().__init__(priority=999)
        self.ctx = ctx

    def handle_authorized_event(self, event):
        logging.info(f'{event.id} was authorized for {self.ctx.authorizer.permission}')

    def handle_unauthorized_event(self, event):
        logging.warn(f'{event.id} was NOT authorized for {self.ctx.authorizer.permission}')

    def handle_none_event(self, event):
        logging.error('Received an event of None, this should not be possible.')


def register(ctx):
    return LoggingHandler(ctx)

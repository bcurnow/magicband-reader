import logging

from magicbandreader.handlers import AbstractHandler


class LoggingHandler(AbstractHandler):
    def handle_authorized_event(self, event):
        logging.info(f'{event.id} was authorized for {event.authorizer.permission}')


    def handle_unauthorized_event(self, event):
        logging.warn(f'{event.id} was NOT authorized for {event.authorizer.permission}')


    def handle_none_event(self, event):
        logging.error('Received an event of None, this should not be possible.')


def register(ctx):
    return LoggingHandler()

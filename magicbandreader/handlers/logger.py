import logging


def handle_authorized_event(event):
    logging.info(f'{event.id} was authorized for {event.permission}')


def handle_unauthorized_event(event):
    logging.warn(f'{event.id} was NOT authorized for {event.permission}')


def handle_none_event(event):
    logging.error('Received an event of None, this should not be possible.')

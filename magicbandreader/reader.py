from collections import namedtuple
import logging

import click
import rfidreader

from magicbandreader.authorize import OpenDoorAuthorizer
from magicbandreader.handlers import register_handlers, EVENT_METHOD_AUTHORIZED, EVENT_METHOD_UNAUTHORIZED, EVENT_METHOD_NONE


Event = namedtuple('Event', ['id', 'authorizer', 'permission'])
_handlers = register_handlers()


@click.command()
@click.option('-u', '--api-url', default='https://192.168.0.42:5000/api/v1.0/', show_default=True, help='The rfid-security-svc base URL')
@click.option('-k', '--api-key', envvar='MR_API_KEY', required=True)
@click.option('--log-level', default='warn')
@click.option('-d', '--device-name', default='/dev/input/rfid', show_default=True, help='The name of the RFID device to read from')
def main(api_url, api_key, log_level, device_name):
    _init_logging(log_level)
    authorizer = OpenDoorAuthorizer(api_url, api_key)
    reader = rfidreader.RFIDReader(device_name)
    while True:
        rfid_id = reader.read()
        event = Event._make([
            rfid_id,
            authorizer,
            authorizer.permission,
            ])
        _handle_event(event, authorizer)


def _handle_event(event, authorizer):
    if event is None:
        handlers = _handlers[EVENT_METHOD_NONE]
    else:
        if authorizer.authorized(event):
            handlers = _handlers[EVENT_METHOD_AUTHORIZED]
        else:
            handlers = _handlers[EVENT_METHOD_UNAUTHORIZED]
    for handler in handlers:
        handler(event)

def _init_logging(log_level):
    numeric_level = getattr(logging, log_level.upper(), None)

    log_warning=False
    if isinstance(numeric_level, int):
        level = numeric_level
    else:
        log_warning = True
        level = logging.WARN

    logging.basicConfig(level=level, format='%(asctime)s %(levelname)s %(message)s')
    if log_warning:
        logging.warn(f'Invalid log level provided "{log_level.upper()}", defaulting to WARN.')

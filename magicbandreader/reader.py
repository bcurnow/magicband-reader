from collections import namedtuple
import logging
from types import SimpleNamespace

import click
import rfidreader

from magicbandreader.authorize import OpenDoorAuthorizer
from magicbandreader.handlers import register_handlers, EventType


Event = namedtuple('Event', ['id', 'authorizer', 'ctx'])


def _validate_volume_level(ctx, param, value):
    if not (value >= 0.0 and value <= 1.0):
        raise click.BadParameter('must be in the range 0.0 - 1.0 (inclusive)')

    if value == 0.0:
        click.secho('Volume set to zero (0), sound will not be audible', fg='red')

    return value


@click.command()
@click.option('-u',
              '--api-url',
              default='https://192.168.0.42:5000/api/v1.0/',
              show_default=True,
              help='The rfid-security-svc base URL.'
              )
@click.option('-k',
              '--api-key',
              envvar='MR_API_KEY',
              required=True,
              help='The API key to authenticate to rfid-security-svc.'
              )
@click.option('--log-level',
              type=click.Choice(['debug', 'info', 'warning', 'error', 'critical'], case_sensitive=False),
              default='warning',
              show_default=True,
              help='The logging level.',
              )
@click.option('-d',
              '--device-name',
              default='/dev/input/rfid',
              show_default=True,
              help='The name of the RFID device.'
              )
@click.option('--volume-level',
              default=.5,
              show_default=True,
              help='The volume sounds should be played at. Range of 0.0 to 1.0 inclusive.',
              callback=_validate_volume_level
              )
@click.pass_context
def main(click_ctx, api_url, api_key, log_level, device_name, volume_level):
    logging.basicConfig(level=getattr(logging, log_level.upper()), format='%(asctime)s %(levelname)s %(message)s')
    ctx = SimpleNamespace(**click_ctx.params)
    handlers = register_handlers(ctx)
    authorizer = OpenDoorAuthorizer(api_url, api_key)
    reader = rfidreader.RFIDReader(device_name)
    while True:
        rfid_id = reader.read()
        event = Event._make([rfid_id, authorizer, ctx])
        event_type = _event_type(event, authorizer)
        for handler in handlers:
            handler.handle_event(event, event_type)


def _event_type(event, authorizer):
    if event is None:
        return EventType.NONE

    if authorizer.authorized(event):
        return EventType.AUTHORIZED

    return EventType.UNAUTHORIZED

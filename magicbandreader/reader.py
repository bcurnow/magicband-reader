import logging
import os
from types import SimpleNamespace

import click
import rfidreader

from magicbandreader.event import Event
from magicbandreader.handlers import register_handlers
from magicbandreader.led import LedController


def _validate_volume_level(ctx, param, value):
    if not (value >= 0.0 and value <= 1.0):
        raise click.BadParameter('must be in the range 0.0 - 1.0 (inclusive)')

    if value == 0.0:
        click.secho('Volume set to zero (0), sound will not be audible', fg='red')

    return value


def _validate_sound_file(ctx, param, sound_file):
    full_path = os.path.join(ctx.params['sound_dir'], sound_file)
    if os.path.exists(full_path):
        return sound_file

    raise click.BadParameter(f'{full_path} does not exist')


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
              default=.1,
              show_default=True,
              help='The volume sounds should be played at. Range of 0.0 to 1.0 inclusive.',
              callback=_validate_volume_level
              )
@click.option('-s',
              '--sound-dir',
              default='/sounds',
              show_default=True,
              help='The directory containing the sound files.'
              )
@click.option('--authorized-sound',
              default='be-our-guest-be-our-guest-put-our-service-to-the-test.wav',
              show_default=True,
              help='The name of the sound file when a band is authorized.',
              callback=_validate_sound_file
              )
@click.option('--unauthorized-sound',
              default='is-my-hair-out.wav',
              show_default=True,
              help='The name of the sound file when a band is unauthorized.',
              callback=_validate_sound_file
              )
@click.pass_context
def main(click_ctx, api_url, api_key, log_level, device_name, volume_level, sound_dir, authorized_sound, unauthorized_sound):
    logging.basicConfig(level=getattr(logging, log_level.upper()), format='%(asctime)s %(levelname)s %(message)s')
    ctx = SimpleNamespace(**click_ctx.params)
    ctx.led_controller = LedController()
    handlers = register_handlers(ctx)
    reader = rfidreader.RFIDReader(device_name)
    logging.info('Waiting for MagicBand...')
    while True:
        rfid_id = reader.read()
        # Need to create the event once, handlers may update attributes
        event = Event(rfid_id, ctx)
        for handler in handlers:
            print(handler)
            handler.handle_event(event)

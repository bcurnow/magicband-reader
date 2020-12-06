import logging
import os
from types import SimpleNamespace

import click
import rfidreader

from magicbandreader.event import Event
from magicbandreader.handlers import register_handlers
from magicbandreader.led import LedController


def _validate_float_percentage_range(ctx, param, value):
    """ Used by the click framework to validate the a range of float values representing percentages."""
    if not (value >= 0.0 and value <= 1.0):
        raise click.BadParameter('must be in the range 0.0 - 1.0 (inclusive)')

    if value == 0.0:
        if param.name == 'brightness_level':
            click.secho('Brightness set to zero (0), no lights will be shown.', fg='red')
        if param.name == 'volume_level':
            click.secho('Volume set to zero (0), sound will not be audible.', fg='red')

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
@click.option('-l',
              '--log-level',
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
@click.option('-v',
              '--volume-level',
              default=.1,
              show_default=True,
              help='The volume sounds should be played at. Range of 0.0 to 1.0 inclusive.',
              callback=_validate_float_percentage_range
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
@click.option('-b',
              '--brightness-level',
              default=.5,
              show_default=True,
              help='The brightness level of the LEDs. Range of 0.0 to 1.0 inclusive.',
              callback=_validate_float_percentage_range
              )
@click.option('-o',
              '--outer-pixel-count',
              default=40,
              show_default=True,
              help='The number of pixels that make up the outer ring.',
              )
@click.option('-i',
              '--inner-pixel-count',
              default=15,
              show_default=True,
              help='The number of pixels that make up the inner ring.'
              )
@click.pass_context
def main(click_ctx, **config):
    ctx = SimpleNamespace(**config)
    logging.basicConfig(level=getattr(logging, ctx.log_level.upper()), format='%(asctime)s %(levelname)s %(message)s')
    ctx.led_controller = LedController()
    handlers = register_handlers(ctx)
    reader = rfidreader.RFIDReader(ctx.device_name)
    logging.info('Waiting for MagicBand...')
    while True:
        rfid_id = reader.read()
        # Need to create the event once, handlers may update attributes
        event = Event(rfid_id, ctx)
        for handler in handlers:
            handler.handle_event(event)

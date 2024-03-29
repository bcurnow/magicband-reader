import logging
import os
from types import SimpleNamespace

import click
import click_config_file
import rfidreader

from magicbandreader.config import yaml_config
from magicbandreader.event import Event
from magicbandreader.handlers import register_handlers
from magicbandreader.led import LedController
from magicbandreader.router import Router


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


@click.command(context_settings=dict(
    max_content_width=500,
    show_default=True,
    auto_envvar_prefix='MR',
    ignore_unknown_options=True,
    allow_extra_args=True))
@click.option('-b',
              '--brightness-level',
              default=.5,
              help='The brightness level of the LEDs. Range of 0.0 to 1.0 inclusive.',
              type=float,
              callback=_validate_float_percentage_range,
              show_envvar=True,
              )
@click_config_file.configuration_option('-c', '--config', implicit=False, help='Read configuration from YAML file.', provider=yaml_config)
@click.option('-i',
              '--inner-pixel-count',
              default=15,
              help='The number of pixels that make up the inner ring.',
              type=int,
              show_envvar=True,
              )
@click.option('-k',
              '--api-key',
              required=True,
              help='The API key to authenticate to rfid-security-svc.',
              show_envvar=True,
              )
@click.option('-l',
              '--log-level',
              type=click.Choice(['debug', 'info', 'warning', 'error', 'critical'], case_sensitive=False),
              default='warning',
              help='The logging level.',
              show_envvar=True,
              )
@click.option('-o',
              '--outer-pixel-count',
              default=40,
              help='The number of pixels that make up the outer ring.',
              type=int,
              show_envvar=True,
              )
@click.option('-p',
              '--permission',
              default='Open Door',
              help='The name of the permission to validate before authorizing.',
              show_envvar=True)
@click.option('-s',
              '--sound-dir',
              default='/sounds',
              help='The directory containing the sound files.',
              show_envvar=True,
              )
@click.option('-t',
              '--reader-type',
              default='mfrc522',
              help='The type of RFID reader implementation to use.',
              show_envvar=True)
@click.option('-u',
              '--api-url',
              default='https://ubuntu-devpi.local:5000/api/v1.0/',
              help='The rfid-security-svc base URL.',
              show_envvar=True,
              )
@click.option('-v',
              '--volume-level',
              default=.1,
              help='The volume sounds should be played at. Range of 0.0 to 1.0 inclusive.',
              type=float,
              callback=_validate_float_percentage_range,
              show_envvar=True,
              )
@click.option('--api-ssl-verify',
              default='ca.pem',
              help='If True or a valid file reference, performs SSL validation, if false, skips validation (this is insecure!).',
              show_envvar=True,
              )
@click.option('--authorized-sound',
              default='authorized.wav',
              help='The name of the sound file played when a band is authorized.',
              callback=_validate_sound_file,
              show_envvar=True,
              )
@click.option('--port-number',
              default=8080,
              help='The port number to listen for request for uid (e.g. from rfid-security-svc).',
              type=click.IntRange(1, 65535),
              show_envvar=True,
              )
@click.option('--read-sound',
              default='read.wav',
              help='The name of the sound file played when a band is read.',
              callback=_validate_sound_file,
              show_envvar=True,
              )
@click.option('--unauthorized-sound',
              default='unauthorized.wav',
              help='The name of the sound file played when a band is unauthorized.',
              callback=_validate_sound_file,
              show_envvar=True,
              )
@click.argument('reader_args', nargs=-1, type=click.UNPROCESSED)
def main(**config):
    ctx = SimpleNamespace(**config)
    logging.basicConfig(level=getattr(logging, ctx.log_level.upper()),
                        format='%(asctime)s %(levelname)s %(pathname)s (line: %(lineno)d): %(message)s'
                        )
    ctx.handlers = register_handlers(ctx)
    logging.debug(f'Handlers: {ctx.handlers}')
    reader = rfidreader.RFIDReader(ctx.reader_type, parse_reader_args(ctx.reader_type, config['reader_args']))
    router = Router(ctx)
    logging.info('Waiting for MagicBand...')
    ctx.led_controller = LedController(brightness=ctx.brightness_level, outer_pixels=ctx.outer_pixel_count, inner_pixels=ctx.inner_pixel_count)
    while True:
        rfid_id = reader.read()
        # There are times when the reader does not return a value. I believe this has to do with not being able to fully
        # power up the tag, probably due to an older tag, make sure we don't attempt to handle this event
        if rfid_id:
            logging.debug(f'Read "{rfid_id}" from the reader')
            # Need to create the event once, handlers may update attributes
            event = Event(rfid_id, ctx)
            router.route(event)


def parse_reader_args(reader_type, args):
    prefix = f'{reader_type}-'
    reader_args = {}
    if not args:
        return reader_args
    if len(args) % 2:
        raise ValueError('Reader arguments must be specified in pairs! Received an odd number of arguments.')
    for i in range(0, len(args), 2):
        if args[i].startswith(prefix):
            reader_args[args[i].removeprefix(prefix)] = args[i + 1]
    return reader_args

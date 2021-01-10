from click import BadParameter
from click.testing import CliRunner
import pytest
import re
from unittest.mock import call, patch

from magicbandreader.event import Event
import magicbandreader.reader


class Parameter:
    """ A testing class that simulates a click Parameter. """
    def __init__(self, name):
        self.name = name


@pytest.mark.parametrize(
    ('param_name', 'value', 'expected', 'message'),
    [
        (Parameter('test'), .5, .5, None),
        (Parameter('test'), -1, BadParameter, re.escape('must be in the range 0.0 - 1.0 (inclusive)')),
        (Parameter('test'), 2, BadParameter, re.escape('must be in the range 0.0 - 1.0 (inclusive)')),
        (Parameter('brightness_level'), 0, 0, 'Brightness set to zero (0), no lights will be shown.'),
        (Parameter('volume_level'), 0, 0, 'Volume set to zero (0), sound will not be audible.'),
    ],
    ids=[
        'success',
        'too low',
        'too high',
        'brightness zero',
        'volume zero'
    ]
    )
def test__validate_float_percentage_range(param_name, value, expected, message):
    if expected is not BadParameter:
        with patch('magicbandreader.reader.click') as click:
            actual = magicbandreader.reader._validate_float_percentage_range(None, param_name, value)
            assert actual == expected
            if message:
                click.secho.assert_called_once_with(message, fg='red')
    else:
        with pytest.raises(BadParameter, match=message):
            magicbandreader.reader._validate_float_percentage_range(None, param_name, value)


@pytest.mark.parametrize(
    ('exists', 'exception_type'),
    [
        (True, None),
        (False, BadParameter),
    ]
    )
@patch('magicbandreader.reader.os')
def test__validate_sound_file(os, exists, exception_type):
    ctx = MockContext({'sound_dir': '/test'})
    os.path.join.return_value = '/test'
    os.path.exists.return_value = exists
    if exception_type:
        with pytest.raises(exception_type, match='/test does not exist'):
            magicbandreader.reader._validate_sound_file(ctx, None, 'test')
    else:
        magicbandreader.reader._validate_sound_file(ctx, None, 'test')
    os.path.join.assert_called_once_with('/test', 'test')
    os.path.exists.assert_called_once_with('/test')


@patch('magicbandreader.reader.Router')
@patch('magicbandreader.reader.register_handlers')
@patch('magicbandreader.reader.rfidreader')
@patch('magicbandreader.reader.LedController')
@patch('magicbandreader.reader.logging')
@patch('magicbandreader.reader.SimpleNamespace')
def test_main(SimpleNamespace, logging, LedController, rfidreader, register_handlers, Router, context):
    led_controller, reader, router = mock_objects_for_main(SimpleNamespace, LedController, rfidreader, register_handlers, context, Router)
    result = CliRunner().invoke(magicbandreader.reader.main, ['-k', 'testing', '--reader-type', 'evdev', 'evdev-device_name', '/dev/input/rfid'])
    assert_result(result)
    assert_logging(logging)
    assert_led(LedController, context, led_controller)
    register_handlers.assert_called_once_with(context)
    rfidreader.RFIDReader.assert_called_once_with('evdev', {'device_name': '/dev/input/rfid'})
    assert_loop(reader, router, context)


@pytest.mark.parametrize(
    ('reader_type', 'args', 'expected'),
    [
        ('evdev', None, {}),
        ('evdev', [], {}),
        ('evdev', ['missing partner'], ValueError),
        ('evdev', ['not-for_you', 'bogus'], {}),
        ('evdev', ['evdev-test_one', 1, 'evdev-test_two', 2], {'test_one': 1, 'test_two': 2}),
    ],
    ids=[
        'No device config',
        'Empty device config',
        'Odd number of options',
        'No device config for type',
        'Some args',
        ]
    )
def test_parse_reader_args(reader_type, args, expected):
    if expected == ValueError:
        with pytest.raises(expected):
            magicbandreader.reader.parse_reader_args(reader_type, args)
    else:
        actual = magicbandreader.reader.parse_reader_args(reader_type, args)
        assert actual == expected


def mock_objects_for_main(SimpleNamespace, LedController, rfidreader, register_handlers, context, Router):
    """ This method takes care of setting up all the mock objects for main and returns the needed ones."""
    SimpleNamespace.return_value = context
    assert not hasattr(context, 'led_controller')
    assert not hasattr(context, 'handlers')
    led_controller = LedController.return_value
    register_handlers.return_value = []
    reader = rfidreader.RFIDReader.return_value
    reader.read.side_effect = ['test_id', BreakTheLoop('This will cause the loop to end.')]
    router = Router.return_value
    return (led_controller, reader, router)


def assert_result(result):
    # Since we threw an IOError, the command should exit with error code 1
    assert result.exit_code == 1
    # The IOError should be wrapped in an OSError
    assert type(result.exception) == BreakTheLoop


def assert_led(LedController, context, led_controller):
    LedController.assert_called_once_with(
        brightness=.5,
        outer_pixels=40,
        inner_pixels=15
    )
    assert hasattr(context, 'led_controller')
    assert context.led_controller == led_controller


def assert_logging(logging):
    logging.basicConfig.assert_called_once_with(
        level=logging.WARNING,
        format='%(asctime)s %(levelname)s %(pathname)s (line: %(lineno)d): %(message)s'
    )
    logging.info.assert_called_once_with('Waiting for MagicBand...')


def assert_loop(reader, router, context):
    assert hasattr(context, 'handlers')
    assert context.handlers == []
    assert reader.read.call_count == 2
    reader.read.assert_has_calls([call(), call()], any_order=False)
    router.route.assert_called_once_with(EqualEvent('test_id', context))


class EqualEvent(Event):
    """ Adds an __eq__ implementation to allow us to assert the call to handle_event."""
    def __eq__(self, other):
        return self.id == other.id and self.ctx == other.ctx


class MockContext:
    def __init__(self, params):
        self.params = params


class BreakTheLoop(Exception):
    pass

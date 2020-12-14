from unittest.mock import call, patch, PropertyMock

import board
import pytest
from magicbandreader.led import LedController, LedColor


DEFAULT_BRIGHTNESS = .5


@patch('magicbandreader.led.neopixel')
@patch('magicbandreader.led.time')
def test__init__(time, neopixel):
    pixels = neopixel.NeoPixel.return_value
    mock_brightness = PropertyMock(name='neopixel.NeoPixel.brightness')
    type(pixels).brightness = mock_brightness
    led = LedController(DEFAULT_BRIGHTNESS, 10, 20)
    assert led.brightness == DEFAULT_BRIGHTNESS
    assert led.outer_pixels == 10
    assert led.inner_pixels == 20
    assert led.pixels == pixels
    neopixel.NeoPixel.assert_called_once_with(board.D18,
                                              30,
                                              brightness=DEFAULT_BRIGHTNESS,
                                              auto_write=False,
                                              pixel_order=neopixel.GRB
                                              )
    assert_blink(time, pixels, mock_brightness, LedColor.WHITE, DEFAULT_BRIGHTNESS, 2, .5)


@patch('magicbandreader.led.neopixel')
@patch('magicbandreader.led.time')
def test_startup_sequence(time, neopixel):
    led, mock_brightness = led_controller(time, neopixel)
    led.startup_sequence()
    assert_blink(time, led.pixels, mock_brightness, LedColor.WHITE, DEFAULT_BRIGHTNESS, 2, .5)


@patch('magicbandreader.led.neopixel')
@patch('magicbandreader.led.time')
def test_blink(time, neopixel):
    led, mock_brightness = led_controller(time, neopixel)
    led.blink(LedColor.WHITE)
    assert_blink(time, led.pixels, mock_brightness, LedColor.WHITE)


@patch('magicbandreader.led.neopixel')
@patch('magicbandreader.led.time')
def test_lights_on(time, neopixel):
    led, mock_brightness = led_controller(time, neopixel)
    led.lights_on(LedColor.WHITE, DEFAULT_BRIGHTNESS)
    mock_brightness.assert_called_once_with(DEFAULT_BRIGHTNESS)
    led.pixels.fill.assert_called_once_with(LedColor.WHITE.value)
    led.pixels.show.assert_called_once()


@patch('magicbandreader.led.neopixel')
@patch('magicbandreader.led.time')
def test_fade_on(time, neopixel):
    led, mock_brightness = led_controller(time, neopixel)
    led.fade_on(LedColor.WHITE, DEFAULT_BRIGHTNESS, sleep_sec=.01)
    assert_has_call_count(led.pixels.fill, call(LedColor.WHITE.value))
    assert_has_call_count(mock_brightness, fade_brightness_changes())
    assert_has_call_count(led.pixels.show, call(), DEFAULT_BRIGHTNESS * 100)
    assert_has_call_count(time.sleep, call(.01), DEFAULT_BRIGHTNESS * 100)


@patch('magicbandreader.led.neopixel')
@patch('magicbandreader.led.time')
def test_lights_off(time, neopixel):
    led, _ = led_controller(time, neopixel)
    led.lights_off()
    led.pixels.fill.assert_called_once_with(0)
    led.pixels.show.assert_called_once()


@patch('magicbandreader.led.neopixel')
@patch('magicbandreader.led.time')
def test_fade_off(time, neopixel):
    led, mock_brightness = led_controller(time, neopixel)
    led.fade_off(brightness=DEFAULT_BRIGHTNESS, sleep_sec=.01)
    assert_has_call_count(mock_brightness, fade_brightness_changes(DEFAULT_BRIGHTNESS, on=False))
    assert_has_call_count(led.pixels.show, call(), (DEFAULT_BRIGHTNESS * 100) + 1)
    assert_has_call_count(time.sleep, call(.01), (DEFAULT_BRIGHTNESS * 100) + 1)
    led.pixels.fill.assert_called_once_with(0)


@patch('magicbandreader.led.neopixel')
@patch('magicbandreader.led.time')
@pytest.mark.parametrize(
    ('sleep_sec', 'reverse', 'effect_width'),
    [
            (.01, False, 8),
            (.01, False, 12),
            (.01, True, 8),
            (20, False, 8),
    ]
    )
def test_color_chase(time, neopixel, sleep_sec, reverse, effect_width):
    led, mock_brightness = led_controller(time, neopixel, outer_pixels=40, inner_pixels=0)
    led.color_chase(LedColor.GREEN, DEFAULT_BRIGHTNESS, sleep_sec=sleep_sec, reverse=reverse, effect_width=effect_width)
    mock_brightness.assert_called_once_with(DEFAULT_BRIGHTNESS)
    assert_has_call_count(led.pixels.__setitem__, color_chase_pixel_changes(LedColor.GREEN, 40, effect_width, reverse))
    assert_has_call_count(led.pixels.show, call(), 40 + effect_width + 1)
    assert_has_call_count(time.sleep, call(sleep_sec), 40 + effect_width)


@pytest.mark.parametrize(
    ('reverse', 'effect_width'),
    [
        (False, 8),
        (False, 12),
        (True, 8),
        (False, 8),
    ]
    )
@patch('magicbandreader.led.neopixel')
@patch('magicbandreader.led.time')
def test_spin(time, neopixel, reverse, effect_width):
    led, mock_brightness = led_controller(time, neopixel, outer_pixels=40, inner_pixels=0)
    led.spin(LedColor.BLUE, DEFAULT_BRIGHTNESS, reverse=reverse, effect_width=effect_width)
    assert_has_call_count(mock_brightness, call(DEFAULT_BRIGHTNESS), 4)
    assert_has_call_count(led.pixels.__setitem__, color_chase_pixel_changes(LedColor.BLUE, 40, effect_width, reverse) * 4)
    assert_has_call_count(led.pixels.show, call(), (40 + effect_width + 1) * 4)
    sleep_calls = [
        *[call(.01)] * (40 + effect_width),
        *[call(.001)] * (40 + effect_width),
        *[call(.0001)] * ((40 + effect_width) * 2),
        ]
    assert_has_call_count(time.sleep, sleep_calls)


def led_controller(time, neopixel, outer_pixels=1, inner_pixels=1):
    led = LedController(DEFAULT_BRIGHTNESS, outer_pixels, inner_pixels)
    # We don't want to keep any of the calls from the constructor
    time.reset_mock(return_value=DEFAULT_BRIGHTNESS)
    neopixel.reset_mock
    led.pixels.reset_mock()
    mock_brightness = PropertyMock(name='neopixel.NeoPixel.brightness')
    type(led.pixels).brightness = mock_brightness
    return (led, mock_brightness)


def assert_blink(time, pixels, mock_brightness, color, brightness=DEFAULT_BRIGHTNESS, iterations=3, sleep_sec=.25):
    # Make sure that the brightness property is being reset to the default
    assert_has_call_count(mock_brightness, call(brightness), iterations + 1)
    assert_has_call_count(pixels.fill, [call(color.value), call(0)], iterations)
    assert_has_call_count(time.sleep, call(sleep_sec), (2 * iterations) - 1)
    assert_has_call_count(pixels.show, call(), iterations * 2)


def assert_has_call_count(mock, calls, count=1):
    expected = []
    total_calls = count

    if isinstance(calls, list):
        total_calls = count * len(calls)
        for _ in range(int(count)):
            for kall in calls:
                expected.append(kall)
    else:
        for _ in range(int(count)):
            expected.append(calls)
    # Check to ensure that the calls were made in order
    mock.assert_has_calls(expected, any_order=False)
    # Check to ensure that all the calls were made
    mock.assert_has_calls(expected, any_order=True)
    # Check to ensure that no additional calls were made
    assert mock.call_count == total_calls


def fade_brightness_changes(target_brightness=DEFAULT_BRIGHTNESS, on=True):
    calls = []
    _end = int(target_brightness * 100) + 1
    if on:
        _range = range(1, _end)
    else:
        _range = reversed(range(_end))
    for current_brightness in _range:
        calls.append(call(current_brightness / 100))
    return calls


def color_chase_pixel_changes(color, outer_pixels, effect_width, reverse=False):
    pixel_changes = []
    for i in range(outer_pixels + effect_width + 1):
        if i <= outer_pixels:
            if reverse:
                pixel_changes.append(call(outer_pixels - i, color.value))
            else:
                pixel_changes.append(call(i, color.value))
        if i >= effect_width:
            if reverse:
                pixel_changes.append(call(outer_pixels - (i - effect_width), 0))
            else:
                pixel_changes.append(call(i - effect_width, 0))
    return pixel_changes

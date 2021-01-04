from unittest.mock import patch, Mock

from magicbandreader.handlers.light_mickey import LightMickeyHandler as Handler, register
from magicbandreader.led import LedColor


def test_Handler___init__(context):
    h = Handler(context)
    assert h.priority == 30
    assert h.ctx == context


@patch('magicbandreader.handlers.light_mickey.threading')
def test_Handler_handle_authorized_event(threading, context, auth_event):
    h = Handler(context)
    t = threading.Thread.return_value
    h.handle_authorized_event(auth_event)
    threading.Thread.assert_called_once_with(target=h._light_mickey, args=(LedColor.GREEN,))
    t.start.assert_called_once()


@patch('magicbandreader.handlers.light_mickey.threading')
def test_Handler_handle_unauthorized_event(threading, context, unauth_event):
    h = Handler(context)
    t = threading.Thread.return_value
    h.handle_unauthorized_event(unauth_event)
    threading.Thread.assert_called_once_with(target=h._light_mickey, args=(LedColor.BLUE,))
    t.start.assert_called_once()


@patch('magicbandreader.handlers.light_mickey.time')
def test_Handler__light_mickey(time, context):
    led = Mock()
    context.led_controller = led
    h = Handler(context)
    h._light_mickey(LedColor.RED)
    led.fade_on.assert_called_once_with(LedColor.RED)
    time.sleep.assert_called_once_with(1)
    led.fade_off.assert_called_once()


def test_register(context):
    h = register(context)
    assert isinstance(h, Handler)

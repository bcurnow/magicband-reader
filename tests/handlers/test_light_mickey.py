from unittest.mock import patch

from magicbandreader.handlers.light_mickey import LightMickeyHandler as Handler, register
from magicbandreader.led import LedColor


def test_Handler___init__(context_with_led_controller):
    h = Handler(context_with_led_controller)
    assert h.priority == 30
    assert h.ctx == context_with_led_controller


@patch('magicbandreader.handlers.light_mickey.threading')
def test_Handler_handle_authorized_event(threading, context_with_led_controller, auth_event):
    h = Handler(context_with_led_controller)
    t = threading.Thread.return_value
    h.handle_authorized_event(auth_event)
    threading.Thread.assert_called_once_with(target=context_with_led_controller.led_controller.fade_on, args=(LedColor.GREEN,))
    t.start.assert_called_once()


@patch('magicbandreader.handlers.light_mickey.threading')
def test_Handler_handle_unauthorized_event(threading, context_with_led_controller, unauth_event):
    h = Handler(context_with_led_controller)
    t = threading.Thread.return_value
    h.handle_unauthorized_event(unauth_event)
    threading.Thread.assert_called_once_with(target=context_with_led_controller.led_controller.fade_on, args=(LedColor.BLUE,))
    t.start.assert_called_once()


def test_register(context):
    h = register(context)
    assert isinstance(h, Handler)

from unittest.mock import patch, Mock

from magicbandreader.handlers.spin import SpinHandler as Handler, register
from magicbandreader.led import LedColor


def test_Handler___init__(context_with_led_controller):
    h = Handler(context_with_led_controller)
    assert h.priority == 0
    assert h.ctx == context_with_led_controller


@patch('magicbandreader.handlers.spin.threading')
def test_Handler_handle_event(threading, context_with_led_controller, auth_event):
    h = Handler(context_with_led_controller)
    t = threading.Thread.return_value
    h.handle_event(auth_event)
    led_controller = context_with_led_controller.led_controller
    threading.Thread.assert_called_once_with(target=h._spin)
    t.start.assert_called_once()
    assert context_with_led_controller.spin_thread == t


def test_Handler__spin(context_with_led_controller):
    h = Handler(context_with_led_controller)
    h._spin()
    led_controller = context_with_led_controller.led_controller
    led_controller.spin.assert_called_once_with(LedColor.WHITE, reverse=True)


def test_register(context_with_led_controller):
    h = register(context_with_led_controller)
    assert isinstance(h, Handler)

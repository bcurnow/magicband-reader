from unittest.mock import patch

from magicbandreader.handlers.turn_off_mickey import TurnOffMickeyHandler as Handler, register


def test_Handler___init__(context_with_led_controller):
    h = Handler(context_with_led_controller)
    assert h.priority == 50
    assert h.ctx == context_with_led_controller


def test_handle_event(context_with_authorization_sound_thread, auth_event):
    h = Handler(context_with_authorization_sound_thread)
    t = context_with_authorization_sound_thread.authorization_sound_thread
    h.handle_event(auth_event)
    t.join.assert_called_once()
    assert not hasattr(context_with_authorization_sound_thread, 'authorization_sound_thread')
    context_with_authorization_sound_thread.led_controller.fade_off.assert_called_once()


@patch('magicbandreader.handlers.turn_off_mickey.logging')
def test_handle_event_no_spin_thread(logging, context_with_led_controller, auth_event):
    h = Handler(context_with_led_controller)
    h.handle_event(auth_event)
    logging.warning.assert_called_once_with('Unable to find authorization_sound_thread in context.')
    context_with_led_controller.led_controller.fade_off.assert_called_once()


def test_register(context_with_led_controller):
    h = register(context_with_led_controller)
    assert isinstance(h, Handler)

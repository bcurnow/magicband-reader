from unittest.mock import call, patch

from magicbandreader.handlers.turn_off_mickey import TurnOffMickeyHandler as Handler, register


def test_Handler___init__(context_with_led_controller):
    h = Handler(context_with_led_controller)
    assert h.priority == 50
    assert h.ctx == context_with_led_controller


def test_handle_event(context_with_all_threads, auth_event):
    h = Handler(context_with_all_threads)
    sound_thread = context_with_all_threads.authorization_sound_thread
    light_thread = context_with_all_threads.light_thread
    h.handle_event(auth_event)
    sound_thread.join.assert_called_once()
    light_thread.join.assert_called_once()
    assert not hasattr(context_with_all_threads, "authorization_sound_thread")
    assert not hasattr(context_with_all_threads, "light_thread")
    context_with_all_threads.led_controller.fade_off.assert_called_once()


def test_handle_event_no_sound_thread(context_with_light_thread, auth_event):
    h = Handler(context_with_light_thread)
    with patch("magicbandreader.handlers.turn_off_mickey.logging") as logging:
        h.handle_event(auth_event)
        logging.warning.assert_called_once_with("Unable to find authorization_sound_thread in context.")
    assert not hasattr(context_with_light_thread, "light_thread")
    context_with_light_thread.led_controller.fade_off.assert_called_once()


@patch("magicbandreader.handlers.turn_off_mickey.logging")
def test_handle_event_no_threads(logging, context_with_led_controller, auth_event):
    h = Handler(context_with_led_controller)
    h.handle_event(auth_event)
    assert logging.warning.call_count == 2
    logging.warning.assert_has_calls(
        [
            call("Unable to find authorization_sound_thread in context."),
            call("Unable to find light_thread in context."),
        ]
    )
    context_with_led_controller.led_controller.fade_off.assert_called_once()


def test_register(context_with_led_controller):
    h = register(context_with_led_controller)
    assert isinstance(h, Handler)

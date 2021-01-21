from magicbandreader.handlers.turn_off_mickey import TurnOffMickeyHandler as Handler, register


def test_Handler___init__(context_with_led_controller):
    h = Handler(context_with_led_controller)
    assert h.priority == 50
    assert h.ctx == context_with_led_controller


def test_handle_event(context_with_led_controller, auth_event):
    h = Handler(context_with_led_controller)
    h.handle_event(auth_event)
    context_with_led_controller.led_controller.fade_off.assert_called_once()


def test_register(context_with_led_controller):
    h = register(context_with_led_controller)
    assert isinstance(h, Handler)

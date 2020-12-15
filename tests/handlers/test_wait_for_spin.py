from unittest.mock import patch

from magicbandreader.handlers.wait_for_spin import WaitForSpinHandler as Handler, register


def test_Handler___init__(context_with_spin_thread):
    h = Handler(context_with_spin_thread)
    assert h.priority == 20
    assert h.ctx == context_with_spin_thread


def test_Handler_handle_event(context_with_spin_thread, auth_event):
    h = Handler(context_with_spin_thread)
    t = context_with_spin_thread.spin_thread
    h.handle_event(auth_event)
    t.join.assert_called_once()
    assert not hasattr(context_with_spin_thread, 'spin_thread')


@patch('magicbandreader.handlers.wait_for_spin.logging')
def test_Handler_handle_event_no_spin_thread(logging, context, auth_event):
    h = Handler(context)
    h.handle_event(auth_event)
    logging.warning.assert_called_once_with('Unable to find spin_thread in context.')


def test_register(context_with_spin_thread):
    h = register(context_with_spin_thread)
    assert isinstance(h, Handler)

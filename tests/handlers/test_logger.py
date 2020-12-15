from unittest.mock import patch

from magicbandreader.handlers.logger import LoggingHandler as Handler, register


def test_Handler___init__(context_with_authorizer):
    h = Handler(context_with_authorizer)
    assert h.priority == 999
    assert h.ctx == context_with_authorizer


@patch('magicbandreader.handlers.logger.logging')
def test_Handler_handle_authorized_event(logging, context_with_authorizer, auth_event):
    h = Handler(context_with_authorizer)
    h.handle_authorized_event(auth_event)
    logging.info.assert_called_once_with(f'{auth_event.id} was authorized for {context_with_authorizer.authorizer.permission}')


@patch('magicbandreader.handlers.logger.logging')
def test_Handler_handle_unauthorized_event(logging, context_with_authorizer, unauth_event):
    h = Handler(context_with_authorizer)
    h.handle_unauthorized_event(unauth_event)
    logging.warn.assert_called_once_with(f'{unauth_event.id} was NOT authorized for {context_with_authorizer.authorizer.permission}')


@patch('magicbandreader.handlers.logger.logging')
def test_Handler_handle_none_event(logging, context_with_authorizer, none_event):
    h = Handler(context_with_authorizer)
    h.handle_none_event(none_event)
    logging.error.assert_called_once_with('Received an event of None, this should not be possible.')


def test_register(context_with_authorizer):
    h = register(context_with_authorizer)
    assert isinstance(h, Handler)

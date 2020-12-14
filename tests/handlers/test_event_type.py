import pytest
from unittest.mock import patch

from magicbandreader.event import Event, EventType
from magicbandreader.handlers.event_type import EventTypeHandler as Handler, register


@patch('magicbandreader.handlers.event_type.RfidSecuritySvcAuthorizer')
def test_Handler___init__(RfidSecuritySvcAuthorizer, context):
    authorizer = RfidSecuritySvcAuthorizer.return_value
    assert not hasattr(context, 'authorizer')
    h = Handler(context, authorizer)
    assert h.priority == 10
    assert hasattr(context, 'authorizer')
    assert context.authorizer == authorizer


@pytest.mark.parametrize(
    ('event', 'authorized', 'event_type'),
    [
        (Event('test_id', None), True, EventType.AUTHORIZED),
        (Event('test_id', None), False, EventType.UNAUTHORIZED),
        (Event(None, None), None, EventType.NONE),
    ]
    )
@patch('magicbandreader.handlers.event_type.RfidSecuritySvcAuthorizer')
def test_Handler_handle_event(RfidSecuritySvcAuthorizer, event, authorized, event_type, context):
    assert event.type is None
    authorizer = RfidSecuritySvcAuthorizer.return_value
    h = Handler(context, authorizer)
    authorizer.authorized.return_value = authorized
    h.handle_event(event)
    if event.id:
        authorizer.authorized.assert_called_once_with(event.id)
    assert event.type == event_type


def test_register(context):
    h = register(context)
    assert isinstance(h, Handler)

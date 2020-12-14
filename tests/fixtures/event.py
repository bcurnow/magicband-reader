import pytest

from magicbandreader.event import Event, EventType


@pytest.fixture
def auth_event(context):
    return Event('test_id', context, EventType.AUTHORIZED)


@pytest.fixture
def unauth_event(context):
    return Event('test_id', context, EventType.UNAUTHORIZED)


@pytest.fixture
def none_event(context):
    return Event('test_id', context, EventType.NONE)

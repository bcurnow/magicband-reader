import pytest

from magicbandreader.event import Event, EventType


@pytest.fixture(scope='session')
def auth_event(context):
    return Event('test_id', context, EventType.AUTHORIZED)


@pytest.fixture(scope='session')
def unauth_event(context):
    return Event('test_id', context, EventType.UNAUTHORIZED)


@pytest.fixture(scope='session')
def none_event(context):
    return Event('test_id', context, EventType.NONE)

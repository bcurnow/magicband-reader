from types import SimpleNamespace

import pytest
from unittest.mock import Mock, PropertyMock


@pytest.fixture(scope='session')
def config():
    return {
        'api_key': 'test key / & with space',
        'api_url': 'test://testing.test',
        'api_ssl_verify': 'sounds like a good idea',
        'authorized_sound': '/test/auth',
        'permission': 'Test',
        'sound_dir': '/test/',
        'unauthorized_sound': '/test/unauth',
        'volume_level': .75,
        }


@pytest.fixture
def context(config):
    return SimpleNamespace(**config)


@pytest.fixture
def context_with_authorizer(context):
    authorizer = Mock()
    type(authorizer).permission = PropertyMock(
        name='context_with_authorizer_authorizer_permission',
        return_value='Test Open Door'
        )
    context.authorizer = authorizer
    return context

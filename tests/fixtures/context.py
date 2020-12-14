from types import SimpleNamespace

import pytest


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


@pytest.fixture(scope='session')
def context(config):
    return SimpleNamespace(**config)

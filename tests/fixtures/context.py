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
        'log_level': 'warning',
        'brightness_level': .5,
        'outer_pixel_count': 40,
        'inner_pixel_count': 15,
        'reader_type': 'evdev',
        'read_sound': '/test/read',
        'port_number': 8080,
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


@pytest.fixture
def context_with_led_controller(context):
    led_controller = Mock()
    context.led_controller = led_controller
    return context


@pytest.fixture
def context_with_spin_thread(context_with_led_controller):
    spin_thread = Mock(name='spin_thread')
    context_with_led_controller.spin_thread = spin_thread
    return context_with_led_controller


@pytest.fixture
def context_with_authorization_sound_thread(context_with_led_controller):
    thread = Mock(name='authorization_sound_thread')
    context_with_led_controller.authorization_sound_thread = thread
    return context_with_led_controller

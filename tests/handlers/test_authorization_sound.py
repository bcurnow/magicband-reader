from unittest.mock import call, patch

from magicbandreader.handlers.authorization_sound import AuthorizationSoundHandler as Handler, register


AUTH_SOUND = object()
UNAUTH_SOUND = object()


@patch('magicbandreader.handlers.authorization_sound.load_sound')
def test_Handler___init__(load_sound, context):
    load_sound.side_effect = [AUTH_SOUND, UNAUTH_SOUND]
    h = Handler(context)
    assert h.priority == 40
    assert h.authorized_sound == AUTH_SOUND
    assert h.unauthorized_sound == UNAUTH_SOUND
    assert load_sound.call_count == 2
    load_sound.assert_has_calls([call(context, context.authorized_sound), call(context, context.unauthorized_sound)], any_order=False)


@patch('magicbandreader.handlers.authorization_sound.play_sound')
@patch('magicbandreader.handlers.authorization_sound.load_sound')
def test_Handler_handle_authorized_event(load_sound, play_sound, context, auth_event):
    t = object()
    play_sound.return_value = t
    h = handler(context, load_sound)
    h.handle_authorized_event(auth_event)
    play_sound.assert_called_once_with(AUTH_SOUND)
    assert context.authorization_sound_thread == t


@patch('magicbandreader.handlers.authorization_sound.play_sound')
@patch('magicbandreader.handlers.authorization_sound.load_sound')
def test_Handler_handle_unauthorized_event(load_sound, play_sound, context, unauth_event):
    t = object()
    play_sound.return_value = t
    h = handler(context, load_sound)
    h.handle_unauthorized_event(unauth_event)
    play_sound.assert_called_once_with(UNAUTH_SOUND)
    assert context.authorization_sound_thread == t


@patch('magicbandreader.handlers.authorization_sound.load_sound')
def test_register(load_sound, context):
    load_sound.side_effect = [AUTH_SOUND, UNAUTH_SOUND]
    h = register(context)
    assert isinstance(h, Handler)


def handler(context, load_sound):
    load_sound.side_effect = [AUTH_SOUND, UNAUTH_SOUND]
    return Handler(context)

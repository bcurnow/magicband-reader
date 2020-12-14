from unittest.mock import call, patch

from magicbandreader.handlers.authorization_sound import AuthorizationSoundHandler as Handler, register


AUTH_SOUND = object()
UNAUTH_SOUND = object()


@patch('magicbandreader.handlers.authorization_sound.play_sound')
@patch('magicbandreader.handlers.authorization_sound.load_sound')
def test_handle_authorized_event(load_sound, play_sound, context, auth_event):
    h = handler(context, load_sound)
    h.handle_authorized_event(auth_event)
    play_sound.assert_called_once_with(AUTH_SOUND)


@patch('magicbandreader.handlers.authorization_sound.play_sound')
@patch('magicbandreader.handlers.authorization_sound.load_sound')
def test_handle_unauthorized_event(load_sound, play_sound, context, unauth_event):
    h = handler(context, load_sound)
    h.handle_unauthorized_event(unauth_event)
    play_sound.assert_called_once_with(UNAUTH_SOUND)


@patch('magicbandreader.handlers.authorization_sound.load_sound')
def test_register(load_sound, context):
    load_sound.side_effect = [AUTH_SOUND, UNAUTH_SOUND]
    h = register(context)
    assert h.priority == 40
    assert h.authorized_sound == AUTH_SOUND
    assert h.unauthorized_sound == UNAUTH_SOUND
    assert load_sound.call_count == 2
    load_sound.assert_has_calls([call(context, context.authorized_sound), call(context, context.unauthorized_sound)], any_order=False)
    assert isinstance(h, Handler)


def handler(context, load_sound):
    load_sound.side_effect = [AUTH_SOUND, UNAUTH_SOUND]
    return Handler(context)

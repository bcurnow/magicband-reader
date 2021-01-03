from unittest.mock import call, patch

from magicbandreader.handlers.read_sound import ReadSoundHandler as Handler, register


READ_SOUND = object()


@patch('magicbandreader.handlers.read_sound.load_sound')
def test_Handler___init__(load_sound, context):
    h = handler(context, load_sound)
    assert h.priority == 0
    assert h.read_sound == READ_SOUND
    load_sound.assert_called_once_with(context, context.read_sound)


@patch('magicbandreader.handlers.read_sound.play_sound')
@patch('magicbandreader.handlers.read_sound.load_sound')
def test_Handler_handle_event(load_sound, play_sound, context):
    h = handler(context, load_sound)
    h.handle_event(None)
    play_sound.assert_called_once_with(READ_SOUND)


@patch('magicbandreader.handlers.read_sound.load_sound')
def test_register(load_sound, context):
    load_sound.return_value = READ_SOUND
    h = register(context)
    assert isinstance(h, Handler)


def handler(context, load_sound):
    load_sound.return_value = READ_SOUND
    return Handler(context)

import os
from types import SimpleNamespace

from unittest.mock import patch

from magicbandreader import audio


CONFIG = {
    'sound_dir': '/test/',
    'volume_level': .75
    }
CTX = SimpleNamespace(**CONFIG)


@patch('magicbandreader.audio.ratio_to_db')
@patch('magicbandreader.audio.AudioSegment')
def test_load_sound(AudioSegment, ratio_to_db):
    expected = AudioSegment.from_file.return_value
    expected.apply_gain.return_value = expected
    ratio_to_db.return_value = CTX.volume_level
    actual = audio.load_sound(CTX, 'test')
    assert actual == expected
    AudioSegment.from_file.assert_called_once_with(os.path.join(CTX.sound_dir, 'test'))
    ratio_to_db.assert_called_once_with(CTX.volume_level)
    expected.apply_gain.assert_called_once_with(CTX.volume_level)


@patch('magicbandreader.audio.threading')
@patch('magicbandreader.audio.play')
def test_play_sound(play, threading):
    sound = object()
    t = threading.Thread.return_value

    ret = audio.play_sound(sound)

    threading.Thread.assert_called_once_with(target=play, args=(sound,))
    t.start.assert_called_once()
    assert ret == t

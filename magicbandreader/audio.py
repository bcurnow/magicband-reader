""" Provides helper functions which wrap pydub (with simpleaudio as the player)."""
import os
import threading
import warnings

# Despite the fact that we are using simpleaudio as our player,
# pydub will still look for ffmpeg/avconv and ffplay/avplay and not find it
# This will suppress those warnings
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    from pydub import AudioSegment
    from pydub.playback import play
    from pydub.utils import ratio_to_db


def load_sound(ctx, sound):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')

        sound = AudioSegment.from_file(os.path.join(ctx.sound_dir, sound))
        # Adjust the volume on the sound based on user input
        sound = sound.apply_gain(ratio_to_db(ctx.volume_level))
        return sound


def play_sound(sound):
    t = threading.Thread(target=play, args=(sound,))
    t.start()
    return t

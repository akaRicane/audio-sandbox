"""Basic script handling the opening of audio files via filepaths,
the import of audio signals via audiogenerator.
Ends with basic plot of read signal.
"""
import os
import sys
import numpy as np
import sounddevice as sd
import soundfile as sf
sys.path.append(os.getcwd())
from lib import config, tool  # noqa E402
from lib import audiodata, audiofile  # noqa E402


if __name__ == "__main__":
    # audio filepath
    filepath = config.AUDIO_FILE_ACID
    # data, fs = audiofile.load_from_filepath(filepath)
    # audiofile.write_in_audiofile(filepath=config.AUDIO_RESSOURCES,
    #                              filename='stereo_file.flac',
    #                              format="FLAC",
    #                              audio_signal=np.random.randn(10, 2),
    #                              rate=44100,
    #                              subtype="PCM_16", overwrite=True)

    # audio contener
    contener = audiodata.AudioData()
    contener.load_audiofile_from_filepath(filepath)
    contener.plot(show=True)

    # sd.play(data, fs)
    # sd.wait()

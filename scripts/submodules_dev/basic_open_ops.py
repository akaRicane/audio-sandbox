"""Basic script handling the opening of audio files via filepaths,
the import of audio signals via audiogenerator.
Ends with basic plot of read signal.
"""
import os
import sys
import numpy
import sounddevice as sd
import soundfile as sf
sys.path.append(os.getcwd())
from lib import config, tool  # noqa E402
from lib import audiodata, audiofile  # noqa E402


if __name__ == "__main__":
    # audio filepath
    filepath = config.AUDIO_FILE_ACID
    data, fs = audiofile.load_from_filepath(filepath, True)

    # audio contener
    contener = audiodata.AudioData(rate=fs)
    contener.tamp = data
    contener.t = numpy.arange(len(data))
    contener.plot(show=True)

    # sd.play(data, fs)
    # sd.wait()

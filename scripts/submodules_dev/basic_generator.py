import os
import sys
import numpy as np
sys.path.append(os.getcwd())
from lib import config, tool  # noqa E402
from lib import audiodata, audiogenerator  # noqa E402


if __name__ == '__main__':
    signal = audiogenerator.Sine(f0=440, gain=0.8,
                                 rate=44100, value=1024,
                                 format='max_size')

    # contener
    contener = audiodata.AudioData(rate=signal.rate)
    contener.t = signal.vect
    contener.tamp = signal.signal
    contener.fft()
    contener.tplot(isNewFigure=True)

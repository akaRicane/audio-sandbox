import os
import sys
import numpy as np
sys.path.append(os.getcwd())
from lib import config, tool  # noqa E402
from lib import audiodata, audiogenerator  # noqa E402


if __name__ == '__main__':
    RATE = 44100
    sine = audiogenerator.Sine(f0=880, gain=0.8,
                               rate=RATE, value=0.5,
                               format='duration')

    multisine = audiogenerator.MultiSine(rate=RATE,
                                         f_list=[100, 440, 7500],
                                         gain_list=[1, 0.3, 0.05],
                                         value=5000)

    noise = audiogenerator.Noise(rate=RATE, gain=1)

    swept = audiogenerator.Sweep(RATE, 100, 1000, 1, value=2)
    # contener
    signal = swept
    contener = audiodata.AudioData(rate=signal.rate)
    contener.t = signal.vect
    contener.tamp = signal.signal
    # contener.fft()
    contener.tplot(isNewFigure=True)

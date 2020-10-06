import numpy as np
from lib import config

def generateSine(f, A, fs=config.SAMPLING_FREQUENCY, duration=config.BASIC_DURATION):
    # init
    w = 2 * np.pi * f  # angular frequency
    N = fs * duration  # nb of points
    # linspace
    t = np.arange(N) / fs

    # sine
    sine =  A * np.sin(w*t)

    return t.tolist(), sine.tolist()
    
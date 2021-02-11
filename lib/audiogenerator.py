import numpy as np
from lib import config


def generateSine(f0: float,
                 gain: float = 1.0,
                 t: list = None,
                 fs=config.SAMPLING_FREQUENCY,
                 duration=config.BASIC_DURATION):
    # init
    w = 2 * np.pi * f0  # angular frequency
    # linspace
    nsamples = int(duration * fs)
    if t is None:
        t = np.linspace(0, duration, nsamples, endpoint=False)
    # sine
    sine = gain * np.sin(w*t)
    return t.tolist(), sine.tolist()


def generateNoisySignal(fs: int = config.SAMPLING_FREQUENCY,
                        t: list = None,
                        duration: float = config.BASIC_DURATION,
                        f0: float = 1000.0):

    nsamples = int(duration * fs)
    if t is None:
        t = np.linspace(0, duration, nsamples, endpoint=False)
    x = 0.1 * np.sin(2 * np.pi * 1.2 * np.sqrt(t))
    x += 0.01 * np.cos(2 * np.pi * 312 * t + 0.1)
    x += 0.02 * np.cos(2 * np.pi * f0 * t + .11)
    x += 0.03 * np.cos(2 * np.pi * 2000 * t)
    return t, x


import numpy as np
import logging
from lib import config, tool


def generateSine(f0: float,
                 gain: float = 1.0,
                 t: list = None,
                 fs=config.SAMPLING_FREQUENCY,
                 duration=config.BASIC_DURATION):
    # init
    w = 2 * np.pi * f0  # angular frequency
    if t is None:
        t = tool.createTemporalLinspace(fs=fs, duration=duration)
    # sine
    sine = gain * np.sin(w*t)
    return t.tolist(), sine.tolist()


def generateMultiSine(f0List: list,
                      gainList: list = None,
                      t: list = None,
                      fs=config.SAMPLING_FREQUENCY,
                      duration=config.BASIC_DURATION):
    # init
    if t is None:
        t = tool.createTemporalLinspace(fs=fs, duration=duration)
    if gainList is None:
        gainList = np.ones(len(f0List))
    # signal creation
    signal = None
    for i in range(len(f0List)):
        _, sine = generateSine(f0=f0List[i], gain=gainList[i], t=t, fs=fs, duration=duration)
        if signal is None:
            signal = sine
        else:
            signal = tool.returnSumOfSignals(signal, sine)
    return t, signal


def generateNoisySignal(fs: int = config.SAMPLING_FREQUENCY,
                        t: list = None,
                        duration: float = config.BASIC_DURATION,
                        f0: float = 1000.0):
    if t is None:
        t = tool.createTemporalLinspace(fs=fs, duration=duration)
    x = 0.1 * np.sin(2 * np.pi * 1.2 * np.sqrt(t))
    x += 0.01 * np.cos(2 * np.pi * 312 * t + 0.1)
    x += 0.02 * np.cos(2 * np.pi * f0 * t + .11)
    x += 0.03 * np.cos(2 * np.pi * 2000 * t)
    return t, x


def generateSweptSine(amp: float = 0.8,
                      f0: float = 20,
                      f1: float = 20000,
                      t: list = None,
                      duration: float = config.BASIC_DURATION,
                      fs: int = config.SAMPLING_FREQUENCY,
                      novak: bool = False):
    """Generates a Sweptsine, from f0 to f1, with a possibility to satisfy novaks conditions (based on https://www.ant-novak.com/publications/papers/2010_ieee_novak.pdf).

    Args:

    Returns:
        
    """

    if t is None:
        t = tool.createTemporalLinspace(fs=fs, duration=duration)

    if novak is True:
        t = None
        L = np.floor( (f0*duration) / np.log(f1/f0) ) / f0
        newDuration = L * np.log(f1/f0)
        t = tool.createTemporalLinspace(fs=fs, duration=newDuration)
        print(f'New duration of the signal has been set to {newDuration} seconds, to satisfy Novak\'s conditions')
    else:
        L = duration / np.log(f1 / f0)

    x = amp * np.sin(2 * np.pi * f0 * L * (np.exp(t / L) - 1))
    
    if len(t)/fs < duration:
        zeroPadding = np.zeros(duration*fs - len(t))
        print(type(zeroPadding))
        x = np.concatenate([x , zeroPadding])
        t = tool.createTemporalLinspace(fs=fs, duration=duration)
        print("Added Zero Padding to the signal to extend it to initial duration")

    return x, t

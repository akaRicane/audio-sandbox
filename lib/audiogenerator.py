import os
import sys
import numpy as np
import logging

sys.path.append(os.getcwd())
from lib import config, tool, errors  # noqa E402


class AudioSignal():
    """ AudioSignal is a (vect, signal) contener
    Usage:
    -> set vect size, rate
    -> add_signal
    """

    def __init__(self):
        self.rate = None
        self.vect = []
        self.signal = []

    def generate_vect(self, value, format: str = 'max_size', rate: int = None):
        if format == 'max_size':
            self.vect = tool.create_linspace(value)
        elif format == 'duration':
            if rate not in config.VALID_SAMPLERATES:
                raise ValueError(errors.INVALID_RATE)
            self.vect = tool.create_time_linspace(rate, value)
        else:
            raise ValueError(f"Format {format} incompatible.\n"
                             "Must be 'max_size' only or 'duration' + rate")

    def add_sine(self):
        return True

    def add_sweep(self):
        pass

    def add_noise(self):
        pass


def generateSine(f0: float,
                 gain: float = 1.0,
                 t: list = None,
                 fs=config.SAMPLING_FREQUENCY,
                 duration=config.BASIC_DURATION):
    # init
    w = 2 * np.pi * f0  # angular frequency
    if t is None:
        t = tool.create_time_linspace(fs=fs, duration=duration)
    # sine
    sine = gain * np.sin(w*np.array(t))
    return t, sine.tolist()


def generateMultiSine(f0List: list,
                      gainList: list = None,
                      t: list = None,
                      fs=config.SAMPLING_FREQUENCY,
                      duration=config.BASIC_DURATION):
    # init
    if t is None:
        t = tool.create_time_linspace(fs=fs, duration=duration)
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
        t = tool.create_time_linspace(fs=fs, duration=duration)
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
                      fade: bool = True,
                      novak: bool = False):
    """Generates a Sweptsine, from f0 to f1, with a possibility to satisfy novaks conditions (based on https://www.ant-novak.com/publications/papers/2010_ieee_novak.pdf).

    Args:
        amp ([float]): [amplitudes of swept sine]
        f0 ([float]): [start frequency (in Hz)]
        f1 ([float]): [end frequency (in Hz)]
        t ([list], optional): [time vector]
        duration ([float]): [Duration (in seconds) of the swept sine, duration may slighty change if novak conditions are respected]
        fs ([int]): [sampling frequency, rate (in Hz)]
        fade ([bool]): [if True, creates a fade in and out on the swept sine]
        novak ([bool]): [imposes novaks condition to Dt between 2 instantaneous frequencies, usefull to easily deconvolute input from output recording, and separate fondamental signal and harmonic signals]

    Returns:
        x ([list]): [list of amplitudes of the swept sine]
        t ([list]): [time vector corresponding to x data]
        
    """

    if t is None:
        t = tool.create_time_linspace(fs=fs, duration=duration)

    if novak is True:
        t = None
        L = np.floor( (f0*duration) / np.log(f1/f0) ) / f0
        newDuration = L * np.log(f1/f0)
        t = tool.create_time_linspace(fs=fs, duration=newDuration)
    else:
        L = duration / np.log(f1 / f0)

    x = amp * np.sin(2 * np.pi * f0 * L * (np.exp(t / L) - 1))

    if fade is True:
        fadeInLength = 0.25*fs
        fadeIn = np.linspace(start=0,stop=1,num=int(fadeInLength))
        fadeOut = np.linspace(start=1,stop=0,num=int(fadeInLength/5))
        window = np.ones(len(x))
        window[0:len(fadeIn)] = fadeIn
        window[len(window)-len(fadeOut):] = fadeOut
        x = x*window
    
    if len(t)/fs < duration:
        zeroPadding = np.zeros(int(duration*fs) - len(t))
        x = np.concatenate([x , zeroPadding])
        t = tool.create_time_linspace(fs=fs, duration=duration)

    return t, x

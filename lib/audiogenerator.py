import os
import sys
import numpy as np

sys.path.append(os.getcwd())
from lib import config, tool, errors  # noqa E402


class AudioSignal:
    """AudioSignal is a (vect, signal) contener
    with fixed sample rate.
    Basis is defined along with format
    """

    def __init__(self, rate: int, value, format='max_size'):
        if rate not in config.VALID_SAMPLERATES:
            raise errors.InvalidRate(
                f"Must be in {config.VALID_SAMPLERATES}")
        self.rate = rate
        self.format = format
        self.generate_vect(value, self.format)

    def generate_vect(self, value, format: str = 'max_size'):
        """Creates a vect usable as x-basis with two methods.
        'max_size' return a value sized-vector.
        'duration' return a vector with a duration of rate*duration.

        Consistency in formats:
        call (rate*duration, 'max_size') == call (duration, 'duration', rate)

        Args:
            value (int or float): [desired lenght in respect of format]
            format (str, optional): [max_size or duration].
                Defaults to 'max_size'

        Returns:
            bool: [whether success]
        """
        success = False
        self.vect = []
        self.format = format
        if self.format == 'max_size':
            self.vect = tool.create_basis(value)
            success = True
        elif self.format == 'duration':
            self.vect = tool.create_time_basis(self.rate, value)
            success = True
        else:
            raise errors.InvalidFormat(
                f"Format {self.format} incompatible.\n"
                "Must be 'max_size' only or 'duration' + rate")
        return success

    def add_signal(self, new_vect, new_data):
        self.signal = tool.sum_arrays(self.signal, new_data)
        return True

    def check_vect_available(self):
        # check if vect available
        if np.size(self.vect) <= 1:
            raise errors.MissingVect("Generate_vect first")

    def check_rate_available(self):
        # check if rate available
        if self.rate is None:
            raise errors.InvalidRate("Specify rate")


class Sine(AudioSignal):
    def __init__(self, rate: int, f0: float, gain: float,
                 value: int = 1024, format: str = 'max_size'):
        """Generate a f0 sine signal at a given rate.
        Class contains the basis vector and the signal.

        Args:
            rate (int): [sample rate]                                                    
            f0 (float): [fundamental frequency (Hz)]
            gain (float): [sine amplitude]
            value (int, optional): [basis size]. Defaults to 1024.
            format (str, optional): [format of basis generation].
                Defaults to 'max_size'.

        Created:
            self.vect (np.array) : [time basis]
            self.signal (np.array) : [sine]
        """
        super().__init__(value=value, format=format, rate=rate)
        # need to convert vect in rad
        self.vect = tool.convert_basis_to_rad(self.vect, self.rate)
        # angular frequency
        w = np.array(2 * np.pi * f0)
        self.vect = w * self.vect
        self.signal = np.multiply(np.sin(self.vect), gain)


class MultiSine(Sine):
    def __init__(self, rate: int, f_list, gain_list: list = None,
                 value: int = 1024, format: str = 'max_size'):
        if gain_list is None:
            gain_list = np.ones(len(f_list)).tolist()
        elif len(f_list) != len(gain_list):
            raise errors.InvalidFormat("f_list and gain_list must"
                                       " have the same length")
        # create first sine
        super().__init__(rate=rate, f0=f_list[0],
                         gain=gain_list[0], value=value,
                         format=format)
        # then, add others one by one
        for idx in range(1, len(f_list)):
            sine_to_add = Sine(rate=self.rate, f0=f_list[idx],
                               gain=gain_list[idx], value=value,
                               format=self.format)
            self.add_signal(sine_to_add.vect, sine_to_add.signal)



def sweep(self):
    pass
def noise(self):
    pass


def generateSine(f0: float,
                 gain: float = 1.0,
                 t: list = None,
                 fs=config.SAMPLING_FREQUENCY,
                 duration=config.DEFAULT_DURATION):
    # init
    # angular frequency
    w = 2 * np.pi * f0
    if t is None:
        t = tool.create_time_linspace(fs=fs, duration=duration)
    # sine
    sine = gain * np.sin(w*np.array(t))
    return t, sine.tolist()


def generateMultiSine(f0List: list,
                      gainList: list = None,
                      t: list = None,
                      fs=config.SAMPLING_FREQUENCY,
                      duration=config.DEFAULT_DURATION):
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
                        duration: float = config.DEFAULT_DURATION,
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
                      duration: float = config.DEFAULT_DURATION,
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

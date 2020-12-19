import logging
import numpy as np
import scipy as sp
from lib import config

def getFft(t, tAmplitude, N=config.FFT_WINDOWING, fs=config.SAMPLING_FREQUENCY):
    """ Return full FFT transform of the given temporal content
    -> output[0] is the zero-frequency sum (sum of the signal) 
    -> [1:int(len(output)/2)] contains the positive frequency terms
    Args:
        t (array of int): [description]
        tAmplitude (array of float): [description]
        N (int, optional): [description]. Defaults to config.FFT_WINDOWING.
        fs (float, optional): [description]. Defaults to config.SAMPLING_FREQUENCY.
    """    
    # freq = fs * np.arange(N) / N
    freq = np.fft.fftfreq(len(t)) * fs
    output = np.fft.fft(tAmplitude)  # output is like ([a1+b1j, a2+b2j, ../])
    amplitude, phase = splitFftVector(output)  
    amplitude_db = 20 * np.log10(amplitude)
    return retCleanFft(freq), retCleanFft(amplitude), retCleanFft(amplitude_db), retCleanFft(phase)

def retCleanFft(x) -> list:
    return x[1:int(len(x)/2)].tolist()

def getiFft(array: list) -> list:
    #TODO fix ifft -> 2 times faster sine vect 4043 -> 2021
    return np.fft.ifft(array)

def getTemporalVector(data, fs=config.SAMPLING_FREQUENCY) -> list:
    return np.arange(start=0, stop=len(data)/fs, step=1/fs)

def splitFftVector(array: list) -> (list, list):
    # amplitude = sqrt( real² + imag²)
    # phase = arctan(imag/real)
    return abs(array), np.arctan(np.imag(array) / np.real(array))

def mergeFftVector(amplitude: list, phase: list) -> list:
    _ = []
    for index in range(len(amplitude)):
        _.append(np.complex(real=amplitude[index], imag=phase[index])) 
    return _

def getBandEnergy(realPart: list, imagPart: list):
    if len(realPart) != len(imagPart):
        logging.info(f"Dimensions are not the same: {len(realPart)} and {len(imagPart)}")
    else:
        _ = 0
        for i, val in enumerate(realPart):
            _ += realPart[i] ** 2 + imagPart[i] ** 2
        ...

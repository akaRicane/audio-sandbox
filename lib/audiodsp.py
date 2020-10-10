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
    freq = fs * np.arange(N) / N
    output = np.fft.fft(tAmplitude)  # output is like ([a1+b1j, a2+b2j, ../])
    amplitude, phase = splitFftVector(output)  
    amplitude_db = 20 * np.log10(amplitude)
    return freq.tolist(), amplitude.tolist(), amplitude_db.tolist(), phase.tolist()

def getiFft(array: list) -> list:
    return np.fft.ifft(array)

def getTemporalVector(data, fs=config.SAMPLING_FREQUENCY) -> list:
    return np.arange(fs * len(data)) / fs

def splitFftVector(array: list) -> (list, list):
    # amplitude = sqrt( real² + imag²)
    # phase = arctan(imag/real)
    return abs(array), np.arctan(np.imag(array) / np.real(array))

def mergeFftVector(amplitude: list, phase: list) -> list:
    _ = []
    for index in range(len(amplitude)):
        _.append(np.complex(real=amplitude[index], imag=phase[index])) 
    return _

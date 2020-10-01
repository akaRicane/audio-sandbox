import numpy as np
import scipy as sp
from lib import config

def getFft(t, tamp, N, fs=config.SAMPLING_FREQUENCY):
    
    f = fs * np.arange((N/2)) / N
    famp = np.fft.fft(tamp)[0:int(N/2)] / N
    fampDb = 20 * np.log10(famp)

    return f, famp, fampDb

def getTemporalVector(data, fs=config.SAMPLING_FREQUENCY):
    return np.arange(fs * len(data)) / fs

def toMono(data):
    return data[0]
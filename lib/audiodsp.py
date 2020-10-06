import numpy as np
import scipy as sp
from lib import config

def getFft(t, tamp, N, fs=config.SAMPLING_FREQUENCY):
    freq = fs * np.arange(N) / N
    output = np.fft.fft(tamp)
    amplitude = abs(output)
    amplitude_db = 20 * np.log10(amplitude)
    phase = np.arctan(np.imag(output) / np.real(output))
    return freq, amplitude, amplitude_db, phase


def getTemporalVector(data, fs=config.SAMPLING_FREQUENCY):
    return np.arange(fs * len(data)) / fs

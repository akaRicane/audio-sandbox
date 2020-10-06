import numpy as np
import scipy as sp
from lib import config

def getFft(t, tAmplitude, N=config.FFT_WINDOWING, fs=config.SAMPLING_FREQUENCY):
    freq = fs * np.arange(N) / N
    output = np.fft.fft(tAmplitude)  # output is like ([a1+b1j, a2+b2j, ../])
    amplitude = abs(output)  # amplitude = sqrt( real² + imag²)
    amplitude_db = 20 * np.log10(amplitude)
    phase = np.arctan(np.imag(output) / np.real(output))  # phase = arctan(imag/real)
    return freq.tolist(), amplitude.tolist(), amplitude_db.tolist(), phase.tolist()


def getTemporalVector(data, fs=config.SAMPLING_FREQUENCY):
    return np.arange(fs * len(data)) / fs
    
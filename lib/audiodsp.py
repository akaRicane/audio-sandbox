import numpy as np
from lib import config, tool


def getFft(tAmplitude, N=config.FFT_WINDOWING, fs=config.SAMPLING_FREQUENCY):  # noqa E501
    """ Return full FFT transform of the given temporal content
    t axis is not required for the operation
    -> output[0] is the zero-frequency sum (sum of the signal)
    -> [1:int(len(output)/2)] contains the positive frequency terms
    We define w the normalized frequency as
    w belongs to [0:1] is equivalent to f belongs to [0:fs]
    we define f [Hz ~ rad/s] = w [rad/sample] * fs [sample/s]
    Args:
        tAmplitude (array of float): [time signal amplitudes]
        N (int, optional): [FFT size]. Defaults to config.FFT_WINDOWING.
        fs (float, optional):
            [sampling frequency]. Defaults to config.SAMPLING_FREQUENCY.

    Returns:
        w ([list]): [cleaned normalized frequencies between [0:0.5] (nyquist)]
        freq ([list]): [cleaned frequency axis]
        amplitude_lin ([list]): [cleaned fft amplitudes vector, linear]
        amplitude_db ([list]): [cleaned fft amplitudes vector, converted in dB]
        phase ([list]): [cleaned phase of signal]
    """
    # freq = fs * np.arange(N) / N
    w = np.fft.fftfreq(len(tAmplitude))
    freq = w * fs
    output = np.fft.fft(tAmplitude)  # output is like ([a1+b1j, a2+b2j, ../])
    amplitude_lin, phase = splitFftVector(output)
    amplitude_db = tool.convertAmpToAmpDb(amplitude_lin)
    return retCleanFft(w), retCleanFft(freq), retCleanFft(amplitude_lin),\
        retCleanFft(amplitude_db), retCleanFft(phase)
    del w, freq, amplitude_lin, amplitude_db, phase


def retCleanFft(x: list) -> list:
    """Returns a cleaned fft vect, e.g. [1:int(len(x)/2)]
    containing the positive frequency terms.
    Works for freqs', amps' and phases'.
    In addition, returns as unique list like [a1, a2, .., an].

    Args:
        x ([list]): [vector returned by FFT]

    Returns:
        list: [1:int(len(x)/2)]
    """
    return x[1:int(len(x)/2)].tolist()


def getiFft(array: list) -> list:
    # TODO fix ifft -> 2 times faster sine vect 4043 -> 2021
    return np.fft.ifft(array)


def getTemporalVector(data, fs=config.SAMPLING_FREQUENCY) -> list:
    """Generate temporal vector of given time signal.
    Format is like [0:1/fs:len(data)/fs].

    Args:
        data ([list]): [time signal]
        fs ([int], optional):
            [sampling frequency]. Defaults to config.SAMPLING_FREQUENCY.

    Returns:
        list: [0:1/fs:len(data)/fs]
    """
    return np.arange(start=0, stop=len(data)/fs, step=1/fs)


def splitFftVector(array: list) -> (list, list):
    """Splits complex fft vector in twice.
    Format is like: [Z = a + i*b] is returned as [amp, phase],
    where:
        amp = abs(Z)
        tan(phase) = imag(Z) / real(Z)
    Opposite function of audiodsp.mergeFftVector().

    Args:
        array (list): [fft in complex form]

    Returns:
        [amplitudes, phase]: [splitted parts returned]
    """
    # amplitude = sqrt( real² + imag²)
    # phase = arctan(imag/real)
    return np.abs(array), np.arctan(np.imag(array) / np.real(array))


def mergeFftVector(amplitude: list, phase: list) -> list:
    """Splits complex fft vector in twice.
    Format is returned like: [Z = amp + i*phase].
    Opposite function of audiodsp.splitFftVector().

    Args:
        amplitude (list): [amplitudes vector]
        phase (list): [phase vector]

    Returns:
        list: [amplitudes + i * phase]
    """
    array = []
    for index in range(len(amplitude)):
        array.append(np.complex(real=amplitude[index], imag=phase[index]))
    return array
    del array


def getBandEnergy(realPart: list, imagPart: list):
    """Computes and returns energy of given frequency band defined
    by its real and imaginary parts.

    Args:
        realPart (list): [real part of fft vector, merged form]
        imagPart (list): [imaginary part of fft vector, merged form]

    Returns:
        [float]: [enregy of frequency band]
    """
    # Parseval theorem https://www.wikiwand.com/en/Spectral_density
    # e * N = sum( abs(real + j*imag) ** 2 ) =  sum(real ** 2 + img ** 2)
    bandEnergy = 0
    for i in range(len(realPart)):
        bandEnergy += realPart[i] ** 2 + imagPart[i] ** 2
    return bandEnergy / len(realPart)
    del bandEnergy, i

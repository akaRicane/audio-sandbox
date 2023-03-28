from pathlib import Path
import soundfile
import sounddevice
import numpy as np
import numpy.fft as fft
import matplotlib.pyplot as plt
import scipy.signal


def keepFftPositiveF(fastft: np.ndarray) -> np.ndarray:
    """keeps only positive frequencies indexes of a fft

    Args:
        fastft (np.ndarray): input fft with positive and negative frequencies

    Returns:
        np.ndarray: output fft with only positive frequency indexes.
    """
    if len(fastft)%2 == 0:
        posfft = fastft[0: int(np.floor(len(fastft)/2)+1)]
    else:
        posfft = fastft[0: int(np.floor(len(fastft)/2)+2)]
    return posfft


def addFftNegativeF(fastft: np.ndarray) -> np.ndarray:
    """Adds the negative frequency indexes to a only positive frequency indexes fft

    Args:
        fastft (np.ndarray): fft with only positive frequency indexes.

    Returns:
        np.ndarray: output complete fft.
    """
    if len(fastft)%2 == 0:
        symFft = np.flip(np.conj(fastft))
        fastft = np.concatenate((fastft, symFft[2:-1]))
    else:
        symFft = np.flip(np.conj(fastft))
        fastft = np.concatenate((fastft, symFft[1:-1]))
    return fastft


def computeFft(x: np.ndarray, n: int=None) -> np.ndarray:
    """Overlay function to compute positive frequency indexes fft

    Args:
        x (np.ndarray): signal.
        n (int, optional): nfft. Defaults to None.

    Returns:
        np.ndarray: fft
    """
    if n is None:
        n = len(x)
    xfft = fft.fft(x, n)
    return keepFftPositiveF(xfft)

def computeIfft(xfft: np.ndarray) -> np.ndarray:
    """Computes temporal signal from positive frequency indexes fft.

    Args:
        xfft (np.ndarray): positive frequency indexes fft

    Returns:
        np.ndarray: temporal signal.
    """
    x = fft.ifft(addFftNegativeF(xfft))
    return x


def frameSignal(x: np.ndarray, frameLength: int, overlapLength: int) -> np.ndarray:
    """Splits signal into multiple chunks with defined overlay size.

    Args:
        x (np.ndarray): Signal.
        frameLength (int): length of each chunk (in indexes).
        overlapLength (int): length of overlapp between each chunk (in indexes).

    Returns:
        np.ndarray: array of chunks.
    """
    framedSignal = []
    indexStatus = 0
    while indexStatus <= len(x)-frameLength:
        framedSignal.append(x[indexStatus:indexStatus+frameLength])
        indexStatus += overlapLength
    framedSignal = np.array(framedSignal)
    framedSignal = np.transpose(framedSignal)
    return framedSignal


def overlapAndAdd(framedSignal: np.ndarray, overlapLength: int, frameLength: int) -> np.ndarray:
    """Contruct temporal signal from array of chunks.

    Args:
        framedSignal (np.ndarray): signal splitted into multiple chunks.
        overlapLength (int, optional): length of overlapp between each chunk (in indexes).
        frameLength (int, optional): length of each chunk (in indexes).

    Returns:
        np.ndarray: temporal signal.
    """
    signal = []
    n = 0
    while n < np.shape(framedSignal)[1]:
        overlapSum = framedSignal[:int(frameLength/2), n] + framedSignal[int(frameLength/2):, n-1]
        signal.append(overlapSum)
        n += 1
    signal = np.concatenate(signal)
    return signal


def computeStft(x: np.ndarray, overlapLength: int, ndft: int) -> np.ndarray:
    """computes short term fourier transform of temporal signal.

    Args:
        x (np.ndarray): signal.
        overlapLength (int): length of overlapp between each chunk (in indexes).
        ndft (int): size of fourier transform.

    Returns:
        np.ndarray: Short term fourier transform.
    """
    framedSignal = frameSignal(x, ndft, overlapLength)
    window = np.sin(np.linspace(0, np.pi, ndft))
    stft = np.zeros((int(ndft/2+1),np.shape(framedSignal)[1]), dtype=complex)
    for n in range(np.shape(stft)[1]):
        stft[:, n] = computeFft(framedSignal[:, n]*window)
    return stft


def computeIstft(stft: np.ndarray, overlapLength: int, ndft: int) -> np.ndarray:
    """Computes signal from stft by applying inverse short term fourier transform.

    Args:
        stft (np.ndarray): Short term fourier transform of a signal.   
        overlapLength (int): length of overlapp between each chunk (in indexes).
        ndft (int): size of fourier transform.

    Returns:
        np.ndarray: _description_
    """
    framedSignal = np.zeros((ndft,np.shape(stft)[1]))
    window = np.sin(np.linspace(0, np.pi, ndft))
    for n in range(np.shape(stft)[1]):
        framedSignal[:, n] = computeIfft(stft[:, n])*window
    signal = overlapAndAdd(framedSignal, overlapLength, ndft)
    return signal


def _processStft(stft: np.ndarray, fs: int, nfft: int):
    """Example function of processing on frequency domain. (low pass filter)

    Args:
        stft (np.ndarray): Short term fourier transform.
        fs (int): sampling frequency.
        nfft (int): fourier transform size.
    """
    b, a = scipy.signal.iirfilter(2, Wn=1000, fs=fs, btype="low", ftype="butter")
    _, h = scipy.signal.freqz(b=b, a=a, worN=int(nfft/2+1), fs=fs)
    for n in range(np.shape(stft)[1]):
        stft[:, n] = h*stft[:, n]


if __name__ == '__main__':
    # input parameters
    nfft = 4096
    hopLength = int(nfft/2)
    # file loading
    audiopath = Path("C:/Users/drew/Documents/audio/resources/moron.wav")
    data, rate = soundfile.read(file=audiopath)
    # make mono
    data = data[:, 0] 
    # STFT
    myStft = computeStft(data, overlapLength=hopLength, ndft=nfft)
    # Processing STFT(not mandatory)
    # _processStft(myStft, rate, nfft)
    # ISTFT
    signal = computeIstft(myStft, overlapLength=hopLength, ndft=nfft)
    # Play signal
    # sounddevice.play(signal, rate)
    # plot signal to compare to original
    plt.figure()
    plt.plot(data)
    plt.plot(signal, linewidth=0.5)
    plt.grid()
    plt.show()

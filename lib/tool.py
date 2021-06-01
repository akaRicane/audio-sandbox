import os
import sys
import copy
import wave
import tempfile
import struct
import numpy as np
sys.path.append(os.getcwd())
from lib import config  # noqa E402


###
# NUMPY COMPLIANT
###


def create_basis(max_size: int = config.DEFAULT_DURATION) -> np.array:
    # numpy linspace
    return np.arange(0, max_size, 1)


def create_time_basis(duration: config.DEFAULT_DURATION,
                      rate: int = config.SAMPLING_FREQUENCY) -> np.array:
    # numpy linspace
    return np.linspace(0, duration, int(duration * rate))


def convert_basis_to_rad(basis: np.array, rate: int):
    return np.array(basis / rate)


def sum_arrays(array1, array2) -> np.array:
    if len(array1) < len(array2):
        # array1 is smaller
        array2, array1 = array1, array2
    # actual sum
    _sum = np.array(np.zeros(len(array1)))
    for i in range(len(array2)):
        _sum[i] = np.add(array1[i], array2[i])

    for ii in range(len(array2), len(_sum)):
        _sum[ii] = array1[ii]
    return _sum

###
# TEMPORARY FILES
###


def save_array_in_temp(array: np.array):
    fd, temp_path = tempfile.mkstemp()
    file = open(temp_path, 'wb')
    file.write(array)
    file.close()
    return fd, temp_path


def load_array_from_temp(temp_path):
    file = open(temp_path, 'rb')
    data = np.frombuffer(file.read(), dtype=np.float64)
    file.close()
    return np.array(data)


def close_tempfile(fd, temp_path):
    file = open(temp_path, 'r')
    file.close()
    os.close(fd)
    os.remove(temp_path)
    return True

###
# OTHERS
###


def return_copy(item):
    return copy.deepcopy(item)


def check_if_file_exist(filepath: str) -> bool:
    return os.path.isfile(filepath)


###
# TODO Clean below
###


def getClosestIndexToTargetInArray(vect: list, target: float) -> list:
    """Returns a list of the array indexes of the closest values,
    regarding a given target.
    In a = [0, 1, 2, 3, 5, 7, 11, 5, 1, 11]
    -> returns [5] if asked getClosest...InArray(a, 7)
    -> returns [4, 7] if asked getClosest...InArray(a, 5)

    Args:
        vect (list): [given vector]
        target (float): [target to match]

    Returns:
        list:
           [list of closest indexes (if more than 2, than all val(i) are same)]
    """
    closestIndexes = []
    minGap = None
    for i, val in enumerate(vect):
        gap = np.abs(float(val - target))
        if gap == minGap:
            closestIndexes.append(i)
        elif minGap is None:
            minGap = gap
        elif gap < minGap:
            closestIndexes = [i]
            minGap = gap
    return closestIndexes


def getBandFrequencies(size: int) -> list:
    # TODO creates musical splitting / 10 bands needed (10 octave is enough)
    # in [A1, ..., G#10] == [A1, A11[
    f0 = config.REF_KEYS_DICT['A0']
    freqList = []
    for idx in range(size):
        freqList.append(f0 * 2 ** (idx + 1))
    return freqList


def convertAmpToAmpDb(amp: list) -> list:
    return 20 * np.log10(amp)


def convertAmpDbToAmp(ampDb: list) -> list:
    return 10 ** (ampDb / 20)


# TODO : Maybe this fonction is not necessary, np.add() does the same thing
def returnSumOfSignals(data1: list, data2: list) -> list:
    result = []
    for idx in range(len(data1)):
        result.append(data1[idx] + data2[idx])
    return result


def convertMonoDatatoWaveObject(data, rate, filename, maximumInteger):
    """ Convert synthetic signal x to bytes object readable by readframes
    function of wave module
    Args:
        [list]:     data,          signal data
        [int]:      rate,       sampling frequency of the signal
        [string]:   filename,   name of the wavfile that will be created
    Returns:
        [class: waveread object]:      bytesData
    """
    obj = wave.open(filename, 'w')
    obj.setnchannels(1)  # mono
    obj.setsampwidth(2)
    obj.setframerate(rate)
    for value in data:
        _bytesdata = struct.pack('<h', int(value*maximumInteger))
        obj.writeframesraw(_bytesdata)
    obj.close()
    bytesData = wave.open(filename, 'r')
    return bytesData


def convertWaveobjectToData(waveobject, maximumInteger):
    # Read file to get buffer
    samples = waveobject.getnframes()
    audio = waveobject.readframes(samples)
    # Convert buffer to float32 with numPy
    audio_int16 = np.frombuffer(audio, dtype=np.int16)
    data = audio_int16.astype(np.float)/maximumInteger
    return data


def bufferBytesToData(bytesData, maximumInteger):
    data = np.frombuffer(bytesData, dtype=np.int16) / maximumInteger
    return data.tolist()


def bufferDataToBytes(data, maximumInteger):
    bytesData = np.array(np.round_(np.array(data)*maximumInteger),
                         dtype=np.int16).tobytes()
    return bytesData


def addToDict(destination: dict, key, data):
    ...

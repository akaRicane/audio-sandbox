import numpy as np
from lib import config


def getClosestIndexToTargetInArray(vect: list, target: float) -> list:
    """Returns a list of the array indexes of the closest values regarding a given target.
    In a = [0, 1, 2, 3, 5, 7, 11, 5, 1, 11]
    -> returns [5] if asked getClosest...InArray(a, 7)
    -> returns [4, 7] if asked getClosest...InArray(a, 5)

    Args:
        vect (list): [given vector]
        target (float): [target to match]

    Returns:
        list: [list of closest indexes (if more than 2, than all val(i) are same)]
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


def getBandFrequencies(size:int) -> list:
    #TODO creates musical splitting / 10 bands needed (10 octave is enough)
    # in [A1, ..., G#10] == [A1, A11[
    f0 = config.REF_KEYS_DICT['A0']
    freqList = []
    for idx in range(size):
        freqList.append(f0 * 2 ** (idx + 1))
    return freqList
    del freqList

def convertAmpToAmpDb(amp: list) -> list:
    return 20 * np.log10(amp)


def convertAmpDbToAmp(ampDb: list) -> list:
    return 10 ** (ampDb / 20)


def addToDict(destination: dict, key, data):
    ...

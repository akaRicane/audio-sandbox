import numpy as np
from lib import config

def getClosestIndexToTargetInArray(vect: list, target: float) -> list:
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
    #TODO creates musical splitting / 10 bands needed
    f0 = config.REF_KEYS_DICT['A0']
    freqList = []
    for idx in range(size):
        freqList.append(f0 * 2 ** (idx + 1))
    return freqList

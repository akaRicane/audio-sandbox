import sys
import os
import copy
import logging
import argparse
from pathlib import Path
import numpy as np

import matplotlib.pyplot as plt

sys.path.append(os.getcwd())
from lib import audio, audioplot, audiofile
from lib import config

# ######################
# #### ARCHITECTURE ####
# ######################
# import audio
# import template
# fourier
# frequency band slicer
# MIR ??
# parametrizer / fit
# filter generation
# other dsp operations
# output audio
# ######################

def getArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=False, help="Audio to be processed regarding template files")
    parser.add_argument("--template", default=False ,help="Audio template file for source processing")
    return parser.parse_args()

def getBandFrequencies(size:int) -> list:
    #TODO creates musical splitting / 10 bands needed
    f0 = config.REF_KEYS_DICT['A0']
    freqList = []
    for idx in range(size):
        freqList.append(f0 * 2 ** (idx + 1))
    return freqList

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

class Slicer():
    def __init__(self, size: int=config.BANDS_SLICER_SIZE, newFreqs: list=None):
        self.size = 10  #TODO to update
        self.bands = {}
        self.freqs = None
        if newFreqs is not None: self.importNewFreqsArray(newFreqs)
    
    def importNewFreqsArray(self, newFreqs: list):
        self.freqs = copy.deepcopy(newFreqs)
        self.freqsLenght = len(self.freqs)
        self.updateSlicer()      

    def getfAmpBandBoudaries(self, bandId: int) -> (int, int):
        return slicer.bands[f'{bandId}']["_freqIdx"][0], \
               slicer.bands[f'{bandId + 1}']["_freqIdx"][0] - 1

    def updateSlicer(self):
        _freqs = copy.deepcopy(self.freqs)
        _bands = {}
        refFreqList = getBandFrequencies(self.size)
        for idx in range(len(refFreqList)):
            _freqIdx = getClosestIndexToTargetInArray(_freqs, refFreqList[idx])
            if len(_freqIdx) == 1:
                boundMin = _freqIdx[0]
            if idx + 1 < len(refFreqList):
                boundMax = getClosestIndexToTargetInArray(_freqs, refFreqList[idx + 1])[0] - 1
            else:
                boundMax = len(_freqs) 
            _bands[f"{idx}"] = {
                "_id": idx,
                "_freqIdx": _freqIdx,
                "_f0": refFreqList[idx],
                "_f": _freqs[boundMin:boundMax]
            }
        self.freqs = copy.deepcopy(_freqs)
        self.bands = copy.deepcopy(_bands)


if __name__ == "__main__":
    logging.info("--- Begining Masterizer module ---")
    args = getArguments()

    # Would have been nicer way
    # source = audio.AudioItem()
    # source.addChannel()
    # source.data[0] = audio.AudioData()
    # but we simplify
    source = audio.AudioData()
    source.loadAudioFile()
    template = audio.AudioData()
    filePath = Path(os.getcwd(), "sources", "audioFileTest.wav")
    template.loadAudioFile(filePath=filePath)
    source.fft()
    template.fft()

    # band slicer
    slicer = Slicer(newFreqs=source.f)
    slicer.updateSlicer()
    

    minIdx, maxIdx = slicer.getfAmpBandBoudaries(5)
    plt.plot(slicer.bands['5']["_f"], source.fampDb[minIdx:maxIdx])
    plt.show()

    source.fplot()
    template.fplot()
    audioplot.pshow()
    ...
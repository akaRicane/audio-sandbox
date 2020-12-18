import sys
import os
import copy
import logging
import argparse
from pathlib import Path

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
    f0 = config.REF_KEYS_DICT['A0']
    freqList = []
    for idx in range(size):
        freqList.append(f0 * 2 ** (idx + 1))
    return freqList

class Slicer():
    def __init__(self, size: int=config.BANDS_SLICER_SIZE, newFreqs: list=None):
        self.size = size
        self.bands = {}
        self.freqs = None
        if newFreqs is not None: self.importNewFreqsArray(newFreqs)
    
    def importNewFreqsArray(self, newFreqs: list):
        self.freqs = copy.deepcopy(newFreqs)
        self.freqsLenght = len(self.freqs)
        self.updateSlicer()

    def updateSlicer(self):
        _freqs = copy.deepcopy(self.freqs)
        _bands = {}
        refFreqList = getBandFrequencies(self.size)
        for idx in range(len(refFreqList)):
            _bands[f"{idx}"] = {
                "_id": idx,
                "_f0": refFreqList[idx],
                "_f": []
            }
        
        ...


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




    source.fplot()
    template.fplot()
    audioplot.pshow()
    ...
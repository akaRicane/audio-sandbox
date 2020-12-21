import sys
import os
import copy
import logging
import argparse
from pathlib import Path
import numpy as np

import matplotlib.pyplot as plt

sys.path.append(os.getcwd())
from lib import audio, audioplot, audiofile, audiodsp
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
    source.fft()
    source.addSlicer(addAmps=True)

    template = audio.AudioData()
    template.loadAudioFile(filePath=config.AUDIO_FILE_TEST)
    template.fft()
    template.addSlicer(addAmps=True)
    print(source.slicer.computeEnergyOfAreas(ids=[3, 4, 5, 6]))
    source.slicer.plotSpectrumByAreas(ids=[3, 4, 5, 6])
    audioplot.pshow()

    source.fplot()
    template.fplot()
    audioplot.pshow()
    ...
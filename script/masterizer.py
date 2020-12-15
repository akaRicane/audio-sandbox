import sys
import os
import logging
import argparse
from pathlib import Path

import matplotlib.pyplot as plt

sys.path.append(os.getcwd())
from lib import audio, audioplot, audiofile

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
    template = audio.AudioData()
    filePath = Path(os.getcwd(), "sources", "audioFileTest.wav")
    template.loadAudioFile(filePath=filePath)
    source.fft()
    template.fft()
    source.fplot()
    template.fplot()
    audioplot.pshow()
    ...
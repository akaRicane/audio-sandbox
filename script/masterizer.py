import logging
import argparse
import os
import sys
sys.path.append(os.getcwd())
from lib import audioplot, audiodata, config  # noqa E402

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
    parser.add_argument("--source", default=False,
                        help="Audio to be processed regarding template files")
    parser.add_argument("--template", default=False,
                        help="Audio template file for source processing")
    return parser.parse_args()


if __name__ == "__main__":
    logging.info("--- Beginning Masterizer module ---")
    args = getArguments()

    # Would have been nicer way
    # source = audio.AudioItem()
    # source.addChannel()
    # source.data[0] = audio.AudioData()
    # but we simplify

    # first: audio we want to masterize
    source = audiodata.AudioData()
    # source.loadAudioFile()
    source.loadSinus()
    source.fft()
    source.addSlicer()

    # then: audio target e.g. template
    # template = audiodata.AudioData()
    # template.loadAudioFile(filePath=config.AUDIO_FILE_TEST)
    # template.fft()
    # template.addSlicer()

    # source.fplot()
    # template.fplot()
    source.slicer.plotSpectrumByAreas(ids=[1,3,4,6,9])
    audioplot.pshow()
    ...

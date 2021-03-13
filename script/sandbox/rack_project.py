import os
import sys
import wave
import droulib, audiostream
sys.path.append(os.getcwd())
from lib import audioplot, audiofile, audiogenerator  # noqa E402 
from lib import audiodata, audiodsp, audiofiltering  # noqa E402
from lib import tool, config  # noqa E402

"""
    Archi should be like
    1/ select input between file or stream
    2/ créer rack
        le rack doit gérer I/O + rackItems avec
        input -> rack -> output, ET
        input_from_rackitem -> rackiteam_processing -> output_to_next_rackitem
        3/ set nombre channels
    3/ créer un multithread avec 1 thread par canal -> // du dsp
    4/ data_original / data.on_going / data.saved
        avec chacun n dimensions = nchannels
"""


if __name__ == "__main__":
    pass
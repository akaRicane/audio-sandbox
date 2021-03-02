import os
import sys
import wave
import scipy.signal as signal
import droulib, audiostream
sys.path.append(os.getcwd())
from lib import audioplot, audiofile, audiogenerator  # noqa E402 
from lib import audiodata, audiodsp, audiofiltering  # noqa E402
from lib import tool, config  # noqa E402


class AudioRack():

    def __init__(self):
        pass

    def add_new_rack_item(self, module, param):
        self.rack_item_i = module.module(param)

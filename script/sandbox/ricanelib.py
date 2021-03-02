import os
import sys
import wave
import scipy.signal as signal
import droulib, audiostream
sys.path.append(os.getcwd())
from lib import audioplot, audiofile, audiogenerator  # noqa E402 
from lib import audiodata, audiodsp, audiofiltering  # noqa E402
from lib import tool, config  # noqa E402


class Audio_filter_rt():
    def __init__(self, fs: int = config.SAMPLING_FREQUENCY,
                 buffer_size: int = config.FRAMES_PER_BUFFER):
        self.fs = fs
        self.buffer_size = buffer_size
        self.buffer_data = None
        self.dsp_state = "Wait"  # can be Wait, Done, Processing, Saving
        self.memory_size = 1
        self.memory_data = []
        self.audio_filter = audiofiltering.AudioFilter(fs=self.fs)

    def filter_buffer_data(self, export_data: bool = False):
        self.dsp_state = "Processing"  # idea when multithreading, to explore
        self.buffer_data = self.audio_filter.returnFilteredData(self.buffer_data)
        self.dsp_state = "Wait"
        if export_data:
            return self.buffer_data

    def save_in_memory(self):
        if len(self.memory_data) == self.memory_size:
            self.memory_data.pop(0)
        self.memory_data.append(self.buffer_data)

    def set_bandpass(self):
        self.audio_filter.getBandPassSosCoefs(lowcut=150,
                                              highcut=2000,
                                              order=8)

    def set_highpass(self):
        self.audio_filter.getHighPassSosCoefs(fcut=3000,
                                              order=8)

    def init_rt_filtering(self):
        self.audio_filter.compute_sos_zi_response()
        self.buffer_data = 0 * self.audio_filter.zi


class AudioRack():

    def __init__(self):
        pass

    def add_new_rack_item(self, module, param):
        self.rack_item_i = module.module(param)

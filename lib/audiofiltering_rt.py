import os
import sys
import numpy

sys.path.append(os.getcwd())
from lib import audiofiltering  # noqa E402
from lib import config  # noqa E402


class Audio_filter_rt():
    def __init__(self, fs: int = config.SAMPLING_FREQUENCY,
                 buffer_size: int = config.FRAMES_PER_BUFFER):
        self.fs = fs
        self.buffer_size = buffer_size
        self.buffer_data = numpy.zeros(self.buffer_size, dtype=float).tolist()
        self.dsp_state = "Wait"  # can be Wait, Done, Processing, Saving
        self.memory_size = 128
        self.memory_data = numpy.zeros(self.memory_size * self.buffer_size, dtype=float).tolist()
        self.audio_filter = audiofiltering.AudioFilter(fs=self.fs)

    def filter_buffer_data(self, export_data: bool = False):
        self.dsp_state = "Processing"  # idea when multithreading, to explore
        self.buffer_data = self.audio_filter.returnFilteredData(self.buffer_data)
        self.dsp_state = "Wait"
        if export_data:
            return self.buffer_data

    def save_in_memory(self):
        self.memory_data = self.memory_data[self.buffer_size:] \
                           + self.buffer_data

    def set_bandpass(self, lowcut: float, highcut: float, order: int = 2):
        self.audio_filter.getBandPassSosCoefs(lowcut=lowcut,
                                              highcut=highcut,
                                              order=order)

    def set_highpass(self, fcut: float, order: int = 2):
        self.audio_filter.getHighPassSosCoefs(fcut=fcut, order=order)

    def init_rt_filtering(self):
        self.audio_filter.compute_sos_zi_response()
        self.audio_filter.zi = (0 * numpy.array(self.audio_filter.zi)).tolist()

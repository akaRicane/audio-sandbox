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

    def check_chunk_size_or_zeropad(self):
        if len(self.buffer_data) != self.buffer_size:
            # zero padding du pauvre
            size_missing = int((self.buffer_size - len(self.buffer_data)) / 2)
            self.buffer_data = numpy.pad(self.buffer_data, size_missing).tolist()
        else:
            pass

    def check_memory_size_or_zeropad(self):
        if len(self.memory_data) != self.buffer_size * self.memory_size:
            # zero padding du pauvre
            size_missing = int((self.buffer_size * self.memory_size - len(self.memory_data)) / 2)
            self.memory_data = numpy.pad(self.memory_data, size_missing).tolist()
        else:
            pass

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

    def get_past_chunk(self, index: int) -> list:
        return self.memory_data[index * self.buffer_size:(index + 1) * self.buffer_size]

    def feedforward(self, delay: int = 1, magnitude: float = 0.90):
        if delay > self.memory_size:
            delay = self.memory_size
        if magnitude >= 1.0:
            magnitude = 1.0 - 1e-9
        elif magnitude <= 0.0:
            magnitude = 1e-9
        past_buffer = [i * magnitude for i in self.get_past_chunk(delay)]
        self.buffer_data = numpy.add(self.buffer_data, past_buffer).tolist()

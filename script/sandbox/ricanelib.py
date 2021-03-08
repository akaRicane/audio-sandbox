import os
import sys
import wave
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
from tkinter import TclError
import droulib
sys.path.append(os.getcwd())
from lib import audioplot, audiofile, audiogenerator  # noqa E402 
from lib import audiodata, audiodsp, audiofiltering  # noqa E402
from lib import tool, config  # noqa E402


class Spectrum_vizualier():
    def __init__(self, memory_size, buffer_size):
        self.fig, (self.ax, self.ax2) = plt.subplots(2, figsize=(15, 8))
        self.memory_size = memory_size
        self.buffer_size = buffer_size
        self.x2_max = self.buffer_size * self.memory_size
        self.x = np.arange(0, self.buffer_size)
        self.x2 = np.arange(0, self.x2_max)

        self.init_lines()
        self.init_axes()

    def init_lines(self):
        self.line, = self.ax.plot(self.x, np.random.rand(self.buffer_size), '-', lw=2)
        self.line2, = self.ax2.plot(self.x2, np.random.rand(self.x2_max), '-', lw=2)

    def init_axes(self):
        self.ax.set_title("AUDIO WAVEFORM")
        self.ax.set_xlabel("Samples")
        self.ax.set_ylabel("Magnitude")
        self.ax.set_xlim(0, self.buffer_size)
        self.ax.set_ylim(-1, 1)
        plt.setp(self.ax,
                 xticks=[0, int(self.buffer_size / 2), self.buffer_size],
                 yticks=[-1, 1])

        self.ax2.set_title("MEMORY")
        self.ax2.set_xlabel("Full signal memory")
        self.ax2.set_ylabel("Magnitude")
        self.ax2.set_xlim(0, self.x2_max)
        self.ax2.set_ylim(-1, 1)
        plt.setp(self.ax2,
                 xticks=[0, int(self.x2_max / 2), self.x2_max],
                 yticks=[-1, 1])
        plt.show(block=False)

    def populate_plot(self, data_line, data_line2):
        self.line.set_ydata(data_line)
        self.line2.set_ydata(data_line2)
        self.update_plot_content()

    def update_plot_content(self):
        try:
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

        except:
            print("Stream is stopped")
            raise TclError


class PlayerRecorder():
    """ Define rack item module as player recorder module.
    Handles either stream, audiofile or audio array as content.
    Player gathers three content bus:
    - original : as original audio content == input
    - processed : as on_going dsp processing on rack
    - edited : as orignal filtered by last saved version of rack
    Player handles also the stream playback as dj controler
    -> in charge of content provided to output stream
    -> in charge of content supplying in rack
    Player can be used both ways:
    - static : loads content and play populates stream
    - dynamic : content is buffer chunk only appending in original
    """
    def __init__(self):
        self.behavior = "static"
        self.behavior_list = ["static", "dynamic"]
        self.player_mode = "loop"
        self.player_mode_list = ["loop", "single"]
        self.player_track = "processed"
        self.player_track_list = ["original", "processed", "edited"]
        self.original = []
        self.processed = None
        self.edited = None
        self.frames_to_read = None
        self.input_file_bytes = None
        self.rate = None
        self.buffer_size = None
        self.max_integer = None
        self.n_channels = None

    def load_wave_object_as_content(self, wave_object, buffer_size):
        self.rate = wave_object.getframerate()
        self.n_channels = wave_object.getnchannels()
        self.frames_to_read = int(buffer_size/self.n_channels)
        self.readable_content = wave_object
        # init first read
        self.read_frames()

    def load_audio_array_as_content(self, audio_array, rate, buffer_size, max_integer):
        # input content
        self.original = audio_array
        self.buffer_size = buffer_size
        self.max_integer = max_integer
        input_file_wave_obj = droulib.convertMonoDatatoWaveObject(audio_array,
                                                                  rate,
                                                                  'test.wav',
                                                                  max_integer)
        self.load_wave_object_as_content(input_file_wave_obj, buffer_size)

    def read_frames(self):
        self.input_file_bytes = self.readable_content.readframes(self.frames_to_read)


class AudioRack():

    def __init__(self):
        pass

    def add_new_rack_item(self, module, param):
        self.rack_item_i = module.module(param)

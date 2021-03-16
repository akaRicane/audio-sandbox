import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import time
from tkinter import TclError
sys.path.append(os.getcwd())
from lib import audioplot, audiofile, audiogenerator  # noqa E402 
from lib import audiodata, audiodsp, audiofiltering  # noqa E402
from lib import audiofiltering_rt as rt_filtering # noqa E402
from lib import audioplot_qt as qt_plot # noqa E402
from lib import player as Player  # noqa E402
from lib import tool, config  # noqa E402


class Spectrum_visualizer():
    def __init__(self, buffer_size, memory_size):
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


class ModulesRack():
    """ Module rack gathering processing modules
    """
    def __init__(self):
        self.chunck = None
        self.module_items = []
        self.wiring = "waterfall"

    def load_and_process_chunck(self, chunk):
        if self.wiring == "waterfall":
            self.chunck = tool.return_copy(chunk)
            self.process_by_parsing_items()

    def process_by_parsing_items(self):
        for module in self.module_items:
            self.chunck = module.process_and_return_chunck(self.chunck)

    def add_new_module(self, *new_module):
        self.module_items.append(*new_module)


class ModuleItem():
    """Module wrapper into module item format
    """
    def __init__(self, type: str = "Audio_filter_rt", subtype: str = "rt_bandpass"):
        self.input = None
        self.output = None
        self.module = None
        self.type = type
        self.subtype = subtype

        if self.type == "Audio_filter_rt":
            if self.subtype == "rt_bandpass":
                self.init_rt_bandpass()
        else:
            pass

    def process_and_return_chunck(self, chunk) -> list:
        self.input = chunk
        if self.type == "Audio_filter_rt":
            if self.subtype == "rt_bandpass":
                self.output = self.module.filter_buffer_data(self.input)
        else:
            self.output = self.input
        return self.output

    def init_rt_bandpass(self):
        self.module = rt_filtering.Audio_filter_rt(LAB_DEFAULT_CONFIG_DICT['SAMPLING_RATE'],
                                                   LAB_DEFAULT_CONFIG_DICT['BUFFER_SIZE'])
        self.module.set_bandpass(lowcut=150, highcut=2500, order=4)
        self.module.init_rt_filtering()


LAB_DEFAULT_CONFIG_DICT = {
    "MAX_INTEGER": 32768.0,
    "BUFFER_SIZE": 1024,
    "SAMPLING_RATE": 44100
}


class Lab():
    """ Higher layer of lab project.
    Basically handles all process.
    Works with rack items.
    Stream is processed by AudioStream instance through Player.
    Processing is handles by audiofitlering_rt instances.
    [AUDIO GENERATOR] / [STREAM IN] / [FILE READ]
    -> [PLAYER] or [MIXER]
        -> [I -> PLAYER(rackitems) -> O]
    -> [RACK ITEMS]
        -> filtering (modules rack)
        -> visualizers (labvisualizer)
        -> edited: input*ModuleRack = output
    """
    def __init__(self):
        self.config = self.load_lab_config()
        self.Player = Player.Player()
        self.LabVisualizer = None
        self.ModulesRack = ModulesRack()
        self.session_is_active = True

    def add_new_module(self, module, param):
        # self.module = module.module(param)
        pass

    def load_lab_config(self):
        pass

    def timeless_loop_static(self):
        """ Aim to manipulate playback in Lab module
        like while true would. Shall handle play pause
        loop and stop in playback somehow.
        Need to make processing through Player.processed
        in rack items.
        """
        # lock input from stream
        # only rack items can be modifiyed from now on
        # freeze.audio.stream()
        while self.session_is_active is True:
            if self.Player.player_mode != "stop":
                # either play mode
                while self.Player.is_end is False:
                    # dsp
                    self.ModulesRack.load_and_process_chunck(self.Player.last_in_original())
                    self.Player.save_processed_buffer(self.ModulesRack.chunck)

                    # playback chunck
                    # self.Player.populate_buffer_in_stream()
                    # continue reading
                    self.Player.read_frames()
                # else wait and see...
                if self.Player.is_end is True and self.Player.player_mode == "single":
                    # self.timeless_sleep()
                    self.Player.player_mode = "stop"
                # or loop again
                elif self.Player.is_end is True and self.Player.player_mode == "loop":
                    time.sleep(0.5)
                    self.Player.restart_read()
            else:
                print("Closing Player")
                self.Player._close()
                break

    def timedef_loop_dynamic(self, duration: float = 5.0):
        start_time = time.time()
        while time.time() <= start_time + duration:
            self.Player.read_frames()
        time.sleep(0.1)

    def record_stream_input_during(self, duration, rate):
        self.Player.init_stream_in(rate)
        self.timedef_loop_dynamic(duration)

    def timeless_sleep(self):
        print("Time to sleep ...")
        self.Player.player_mode = "sleep"
        while self.Player.player_mode == "sleep":
            time.sleep(1)

    def init_labvisualizer(self):
        self.LabVisualizer = qt_plot.LabVisualizer(0, self.Player.original, self.Player.processed)

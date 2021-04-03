import os
import sys
import time

import ricanelib

sys.path.append(os.getcwd())
from lib import audioplot_qt as qt_plot  # noqa E402
from modules import audiofiltering_rt as rt_filtering # noqa E402
from modules import player as Player  # noqa E402


class AudioCore():
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
        self.Visualizer = None  # TODO move to gui handler
        self.ModulesRack = ricanelib.ModulesRack()
        self.session_is_active = True

    def load_lab_config(self):
        pass

    def run(self):  # TODO move to gui handler
        self.Player.AudioStream.init_static_stream()
        self.timeless_loop_static()

    ##########
    # manipulate Player
    ##########

    def timeless_loop_static(self):
        """ Aim to manipulate playback in Lab module
        like while true would. Shall handle play pause
        loop and stop in playback somehow.
        Need to make processing through Player.processed
        in rack items.
        """
        while self.session_is_active is True:
            if self.Player.player_mode != "stop":
                # either play mode
                while self.Player.is_end is False:
                    # dsp
                    self.ModulesRack.load_and_process_chunk(self.Player.last_in_original())
                    self.Player.save_processed_buffer(self.ModulesRack.chunk)

                    # playback chunk
                    # self.Player.populate_buffer_in_stream()
                    # continue reading
                    self.Player.read_frames(bypass=True)
                    self.Visualizer.update(self.Player.read_chunk)
                # else wait and see...
                if self.Player.is_end is True and self.Player.player_mode == "single":
                    # self.timeless_sleep()
                    self.Player.player_mode = "sleep"
                # or loop again
                elif self.Player.is_end is True and self.Player.player_mode == "loop":
                    time.sleep(0.5)
                    self.Player.restart_read()
            else:
                print("Closing Player")
                # self.thread.join()
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

    ##########
    # manipulate ModuleRack
    ##########

    def add_new_module(self, module, param):
        # self.module = module.module(param)
        pass

    def init_labvisualizer(self):
        self.LabVisualizer = qt_plot.LabVisualizer(0, self.Player.original, self.Player.processed)

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
        self.session_is_muted = True
        self.session_visualizer_is_active = False

    def load_lab_config(self):
        pass

    def run(self):  # TODO move to gui handler
        self.Player.AudioStream.init_static_stream()
        self.timeless_loop_static()

    ##########
    # manipulate Player : STATIC
    ##########
    def play_once_until_end(self):
        """ Read all frames until player.is_end is False"""
        print("Play_once_until_end running")
        while self.Player.is_end is False:
            # remember a first read_frames is always done in init
            # dsp
            # self.ModulesRack.load_and_process_chunk(self.Player.last_in_original())
            # self.Player.save_processed_buffer(self.ModulesRack.chunk)

            # reading
            self.Player.read_frames_from_waveobject(bypass=False)

            # playback chunk
            if not self.session_is_muted:
                self.Player.populate_buffer_in_stream()

            # populate visualizer
            if self.session_visualizer_is_active:
                self.Visualizer.update(self.Player.read_chunk)

    def timeless_loop_static(self):
        """ Aim to manipulate playback in Lab module
        like while true would. Shall handle play pause
        loop and stop in playback somehow.
        Need to make processing through Player.processed
        in rack items.
        """
        self.Player.AudioStream.init_stream()
        while self.session_is_active is True:
            if self.Player.player_mode == "stop":
                print("Closing Player")
                self.Player._close()
                break
            else:
                # play content
                self.play_once_until_end()
                if self.Player.player_mode == "single":
                    # put in sleep after played once
                    self.Player.player_mode = "sleep"
                # or loop again
                elif self.Player.player_mode == "loop":
                    time.sleep(0.1)
                    self.Player.restart_read()
                # or sleep
                elif self.Player.player_mode == "sleep":
                    self.timeless_sleep()
                else:
                    if self.Player.player_mode not in self.Player.player_mode_list:
                        print(f"Selected player_mode is undefined: {self.Player.player_mode}")
                    else:
                        print("Undefined error with player mode")
                    self.Player.player_mode = "stop"

    def timeless_sleep(self):
        print("Time to sleep ...")
        self.Player.player_mode = "sleep"
        while self.Player.player_mode == "sleep":
            time.sleep(0.5)

    ##########
    # manipulate Player : DYNAMIC
    ##########

    def timedef_loop_dynamic(self, duration: float = 5.0):
        self.Player.AudioStream.init_stream()
        start_time = time.time()
        while time.time() <= start_time + duration:
            self.Player.AudioStream.unpack_stream()
        time.sleep(0.1)

    def record_stream_input_during(self, duration: float, rate: int):
        print("Start recording input stream session")
        self.Player.config_stream_in(rate)
        if duration <= 0.0:
            # timeless loop
            pass  # TODO timeless recording in
        else:
            self.timedef_loop_dynamic(duration)
        print("Record is done. Now processing ...")
        # store whatever been recorded in original
        self.Player.original = self.Player.AudioStream.data_in
        print("Processing done.")

    ##########
    # manipulate ModuleRack
    ##########

    def add_new_module(self, module, param):
        # self.module = module.module(param)
        pass

    def init_labvisualizer(self):
        self.LabVisualizer = qt_plot.LabVisualizer(2, self.Player.original, self.Player.processed)

import os
import sys
import pyaudio
import droulib
sys.path.append(os.getcwd())
from lib import tool, config  # noqa E402


class AudioStream():
    def __init__(self):
        self.player = None
        self.stream = None
        self.n_channels = None
        self.read_audio_from_system = False
        self.play_audio_on_system = False
        self.stream_rate = config.SAMPLING_FREQUENCY
        self.buffer_size = config.FRAMES_PER_BUFFER
        self.bytes_format = config.BYTES_DEFAULT_FORMAT

    def init_new_stream(self):
        self.player = pyaudio.PyAudio()
        self.stream = self.player.open(format=self.bytes_format,
                                       channels=self.n_channels,
                                       rate=self.stream_rate,
                                       input=self.read_audio_from_system,
                                       output=self.play_audio_on_system,
                                       frames_per_buffer=self.buffer_size)

    def close_stream(self):
        self.pause_playback()
        self.stream.close()
        self.player.terminate()

    def populate_playback(self, data):
        self.stream.write(data, self.buffer_size)

    def pause_playback(self):
        self.stream.stop_stream()

    def update_buffer_size(self, new_size: int):
        self.buffer_size = new_size

    def update_stream_rate(self, new_rate: int):
        self.rate = new_rate

    def update_n_channels(self, new_number):
        self.n_channels = new_number

    def activate_playback(self):
        self.play_audio_on_system = True

    def mute_playback(self):
        self.play_audio_on_system = True

    def update_stream_parameters(self):
        self.stream.close()
        self.stream = self.player.open(format=self.bytes_format,
                                       channels=self.n_channels,
                                       rate=self.stream_rate,
                                       input=self.read_audio_from_system,
                                       output=self.play_audio_on_system,
                                       frames_per_buffer=self.buffer_size)

import os
import sys
import pyaudio
import droulib
sys.path.append(os.getcwd())
from lib import tool, config  # noqa E402


class AudioStream():
    """Audio Stream is an object handling i/o audio interface
    with running operating system. Uses pyaudio lib as player
    interface. Stream object handles the bus gathering 
    audio in -> stream -> audio output.

    Read_audio_from_system to True activates the read of audio in
    Play_audio_on_system to True activates the playback of current stream

    my_stream = AudioStream()
    my_stream.init_new_stream() opens new stream
    my_stream.populate_playback(data) add data array to playback stream
    my_stream.update() terminate current to init new stream with new parameters.
    """
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

import os
import sys
import struct
import pyaudio
import numpy
sys.path.append(os.getcwd())
from lib import tool, config  # noqa E402


class AudioStream():
    """Audio Stream is an object handling i/o audio interface
    with running operating system. Uses pyaudio lib as player
    interface. Stream object handles the bus gathering
    audio in -> stream -> audio output.

    Read_audio_from_system to True activates the read of audio in
    Play_audio_on_system to True activates the playback of current stream
        by default true

    my_stream = AudioStream()
    my_stream.init_###_stream() opens new stream
    my_stream.populate_playback(data) add data array to playback stream
    my_stream.update() terminate current to init new stream with new parameters.
    """
    def __init__(self,
                 n_channels: int,
                 read_audio_from_system: bool = True,
                 play_audio_on_system: bool = True,
                 stream_rate: int = config.SAMPLING_FREQUENCY,
                 buffer_size: int = config.FRAMES_PER_BUFFER):
        self.player = pyaudio.PyAudio()
        self.read_audio_from_system = read_audio_from_system
        self.play_audio_on_system = play_audio_on_system
        self.n_channels = n_channels
        self.stream_rate = stream_rate
        self.buffer_size = buffer_size
        self.bytes_format = config.BYTES_DEFAULT_FORMAT
        self.callback = None
        self.data_in = None

    ##########
    # init stream
    ##########

    def init_stream(self):
        self.stream = self.player.open(format=self.bytes_format,
                                       channels=self.n_channels,
                                       rate=self.stream_rate,
                                       input=self.read_audio_from_system,
                                       output=self.play_audio_on_system,
                                       frames_per_buffer=self.buffer_size)

    ##########
    # manipulate stream
    ##########

    def close_stream(self):
        # self.pause_playback()
        self.stream.close()
        self.player.terminate()

    def populate_playback(self, data):
        self.stream.write(data, self.buffer_size)

    def activate_playback(self):
        self.play_audio_on_system = True
        self.update_stream_parameters()

    def mute_playback(self):
        self.play_audio_on_system = False
        self.update_stream_parameters()

    def pause_playback(self):
        self.stream.stop_stream()

    def unpack_stream(self):
        data_in = self.stream.read(self.buffer_size)
        data_in = struct.unpack(str(2 * self.buffer_size) + 'B', data_in)
        data_in = numpy.array(data_in, dtype='b')[::2]
        self.data_in = data_in.tolist()

    ##########
    # update stream parameters
    ##########

    def update_buffer_size(self, new_size: int):
        self.buffer_size = new_size

    def update_stream_rate(self, new_rate: int):
        self.rate = new_rate

    def update_n_channels(self, new_number):
        self.n_channels = new_number

    def update_stream_parameters(self):
        self.pause_playback()
        self.stream.close()
        self.stream = self.player.open(format=self.bytes_format,
                                       channels=self.n_channels,
                                       rate=self.stream_rate,
                                       input=self.read_audio_from_system,
                                       output=self.play_audio_on_system,
                                       frames_per_buffer=self.buffer_size,
                                       stream_callback=self.callback)

    ##########
    # callback methods
    ##########

    def update_callback(self, callback_method):
        self.callback = callback_method()

import os
import sys
import wave
sys.path.append(os.getcwd())
from lib import audiostream, tool, config  # noqa E402


class Player():
    """ Define rack item module as player (recorder) module.
    Handles either stream in, audiofile or audio array as content.
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
    def __init__(self, filepath: str = None):
        # MANDATORY ATTRIBUTES
        self.rate = None
        self.n_channels = None
        self.buffer_size = 1024
        self.max_integer = 32768.0
        # ITSELF INSTANCE ATTRIBUTES
        self.behavior = "static"
        self.behavior_list = ["static", "dynamic"]
        self.player_mode = "single"
        self.player_mode_list = ["loop", "single", "sleep", "stop"]
        self.player_track = "original"
        self.player_track_list = ["original", "processed", "edited"]
        self.original = []
        self.processed = []
        self.edited = None
        # STREAM
        self.frames_to_read = None
        self.read_bytes = None
        self.read_chunk = None
        self.readable_content = None
        self.is_end = False

    ##########
    # init stream with specific behavior
    ##########

    def config_stream_with_filepath(self, filepath):
        self.load_wav_from_filepath(filepath)
        self.AudioStream = audiostream.AudioStream(n_channels=self.n_channels,
                                                   stream_rate=self.readable_content.getframerate(),
                                                   buffer_size=self.buffer_size)

    def config_stream_with_audio_array(self, audio_array: list, rate: int):
        self.load_audio_array_as_content(audio_array, rate)
        self.AudioStream = audiostream.AudioStream(n_channels=self.n_channels,
                                                   stream_rate=self.readable_content.getframerate(),
                                                   buffer_size=self.buffer_size)

    def config_stream_in(self, rate):
        self.behavior = "dynamic"
        self.rate = rate
        self.AudioStream = audiostream.AudioStream(n_channels=1,
                                                   read_audio_from_system=True,
                                                   stream_rate=self.rate)

    ##########
    # load audio content
    ##########

    def load_wav_from_filepath(self, filepath):
        f = wave.open(filepath.__str__(), 'r')
        self.load_wave_object_as_content(f, self.buffer_size)

    def load_wave_object_as_content(self, wave_object, buffer_size):
        self.rate = wave_object.getframerate()
        self.n_channels = wave_object.getnchannels()
        self.frames_to_read = int(buffer_size/self.n_channels)
        self.readable_content = wave_object
        # init first read
        self.read_frames(bypass=False)

    def load_audio_array_as_content(self, audio_array, rate):
        input_file_wave_obj = tool.convertMonoDatatoWaveObject(audio_array,
                                                               rate,
                                                               'resources/bin/test.wav',
                                                               self.max_integer)
        self.load_wave_object_as_content(input_file_wave_obj, self.buffer_size)

    ##########
    # manipulate stream content
    ##########

    def read_frames(self, bypass: bool = False):
        self.read_bytes = self.readable_content.readframes(self.frames_to_read)
        self.raise_if_end()
        self.read_chunk = tool.bufferBytesToData(self.read_bytes, self.max_integer)
        if bypass is False:
            self.original += self.read_chunk

    def populate_buffer_in_stream(self):
        if self.player_track == "original":
            buffer_streamed = self.last_in_original()
        elif self.player_track == "processed":
            buffer_streamed = self.last_in_processed()
        else:
            # add handle edited playback
            buffer_streamed = self.last_in_original()
        self.AudioStream.populate_playback(tool.bufferDataToBytes(buffer_streamed, self.max_integer))

    def raise_if_end(self):
        if self.read_bytes == b'':
            self.is_end = True
            print("Player.is_end passed to False")
        else:
            pass

    def last_in_original(self):
        return self.original[-self.buffer_size:-1]

    def last_in_processed(self):
        return self.processed[-self.buffer_size:-1]

    ##########
    # filtering manipulations
    ##########

    def save_processed_buffer(self, processed_buffer: list):
        self.processed += processed_buffer

    def render_edited_content(self, rack):
        pass

    ##########
    # manipulate player
    ##########

    def restart_read(self):
        self.is_end = False
        self.readable_content.rewind()

    def _mute(self):
        # TODO add on click method
        self.AudioStream.mute_playback()

    def _play(self):
        # TODO add on click method
        self.AudioStream.activate_playback()

    def _close(self):
        # TODO add on click method
        self.AudioStream.close_stream()

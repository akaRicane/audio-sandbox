import os
import sys
import wave
import droulib, audiostream
sys.path.append(os.getcwd())
from lib import audioplot, audiofile, audiogenerator  # noqa E402 
from lib import audiodata, audiodsp, audiofiltering  # noqa E402
from lib import tool, config  # noqa E402


def play_file_from_filepath(filepath):
    f = wave.open(filepath.__str__(), 'r')

    print("open stream")
    my_stream = audiostream.AudioStream()
    my_stream.update_buffer_size(BUFFER_SIZE)
    my_stream.update_n_channels(f.getnchannels())
    my_stream.update_stream_rate(f.getframerate())
    my_stream.activate_playback()

    print(f"Framerate: {f.getframerate()} samples/sec")
    my_stream.init_new_stream()
    input_file_bytes = f.readframes(int(BUFFER_SIZE/f.getnchannels()))
    # format is byte
    while input_file_bytes != b'':
        # -- POSSIBLE DSP ON input_file_bytes --

        # -- END OF DSP --
        # format is byte
        my_stream.populate_playback(input_file_bytes)
        input_file_bytes = f.readframes(int(BUFFER_SIZE/f.getnchannels()))
    print("End of file")
    my_stream.close_stream()


def play_from_audio_array(audio_array, rate):
    print("open stream")
    my_stream = audiostream.AudioStream()
    my_stream.update_buffer_size(BUFFER_SIZE)
    my_stream.update_n_channels(1)
    my_stream.update_stream_rate(rate)
    my_stream.activate_playback()

    print(f"Framerate: {rate} samples/sec")
    my_stream.init_new_stream()
    input_file_wave_object = droulib.convertMonoDatatoWaveObject(audio_array,
                                                           rate,
                                                           'test.wav',
                                                           32768.0)
    input_file_bytes = input_file_wave_object.readframes(int(BUFFER_SIZE/input_file_wave_object.getnchannels()))
    while input_file_bytes != b'':
        # -- POSSIBLE DSP ON INPUT_FILE_FRAME --

        # -- END OF DSP --
        my_stream.populate_playback(input_file_bytes)
        input_file_bytes = input_file_wave_object.readframes(int(BUFFER_SIZE/input_file_wave_object.getnchannels()))

    print("End of file")
    my_stream.close_stream()


if __name__ == "__main__":
    # Global Parameters
    BUFFER_SIZE = 1024
    sweep, tsweep = audiogenerator.generateSweptSine(amp=0.5,
                                                     f0=150,
                                                     f1=10000,
                                                     duration=2.0,
                                                     fs=config.SAMPLING_FREQUENCY,
                                                     fade=True,
                                                     novak=True)
    play_from_audio_array(sweep, config.SAMPLING_FREQUENCY)
    # load audio as wave_read object
    read_filepath = config.AUDIO_FILE_TEST
    play_file_from_filepath(read_filepath)
    ...

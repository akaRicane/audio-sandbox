import os
import sys
import wave
import numpy as np
import matplotlib.pyplot as plt
import time
import droulib
import ricanelib
sys.path.append(os.getcwd())
from lib import audioplot, audiofile, audiogenerator  # noqa E402 
from lib import audiodata, audiodsp, audiofiltering  # noqa E402
from lib import audiofiltering_rt as rt_filtering # noqa E402
from lib import audiostream, tool, config  # noqa E402


def play_file_from_filepath(filepath):
    f = wave.open(filepath.__str__(), 'r')
    BUFFER_SIZE = 1024
    print("open stream")
    my_stream = audiostream.AudioStream()
    my_stream.update_buffer_size(BUFFER_SIZE)
    my_stream.update_n_channels(f.getnchannels())
    my_stream.update_stream_rate(f.getframerate())
    print("stream opened")
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
    MAX_INTEGER = 32768.0
    BUFFER_SIZE = int(1024)
    print(f"Framerate: {rate} samples/sec")

    # filtrage item
    my_rt_filter = rt_filtering.Audio_filter_rt(rate, BUFFER_SIZE)
    my_rt_filter.set_bandpass(lowcut=150, highcut=2500, order=4)
    # my_rt_filter.set_highpass(fcut=2000, order=2)
    my_rt_filter.init_rt_filtering()

    # my_rt_filter.audio_filter.computeFilterFreqResp()
    # my_rt_filter.audio_filter.plotFilterResponse()

    # plotting definition
    visualizer = ricanelib.Spectrum_vizualier(memory_size=my_rt_filter.memory_size,
                                              buffer_size=my_rt_filter.buffer_size)

    print("open stream")
    my_stream = audiostream.AudioStream(n_channels=1,
                                        stream_rate=rate,
                                        buffer_size=BUFFER_SIZE)
    my_stream.init_array_stream()

    # input content
    input_file_wave_object = droulib.convertMonoDatatoWaveObject(audio_array,
                                                                 rate,
                                                                 'test.wav',
                                                                 MAX_INTEGER)

    frames_to_read = int(BUFFER_SIZE/input_file_wave_object.getnchannels())
    input_file_bytes = input_file_wave_object.readframes(frames_to_read)

    while input_file_bytes != b'':
        my_rt_filter.buffer_data = droulib.bufferBytesToData(input_file_bytes, MAX_INTEGER)
      
        if len(my_rt_filter.buffer_data) != my_rt_filter.buffer_size:
            # zero padding du pauvre
            size_missing = int((my_rt_filter.buffer_size - len(my_rt_filter.buffer_data)) / 2)
            my_rt_filter.buffer_data = np.pad(my_rt_filter.buffer_data, size_missing).tolist()
        if len(my_rt_filter.memory_data) != my_rt_filter.buffer_size * my_rt_filter.memory_size:
            # zero padding du pauvre
            size_missing = int((my_rt_filter.buffer_size * my_rt_filter.memory_size - len(my_rt_filter.memory_data)) / 2)
            my_rt_filter.memory_data = np.pad(my_rt_filter.memory_data, size_missing).tolist()
   
        # -- POSSIBLE DSP ON INPUT_FILE_FRAME --
        # my_rt_filter.filter_buffer_data()
        my_rt_filter.feedforward(delay=64)
        # -- END OF DSP --
        my_rt_filter.save_in_memory()
        # playback filtered chunk
        my_stream.populate_playback(droulib.bufferDataToBytes(my_rt_filter.buffer_data, MAX_INTEGER))

        # plotting
        # visualizer.populate_plot(data_line=my_rt_filter.buffer_data, data_line2=my_rt_filter.memory_data)
        # load new chunk
        input_file_bytes = input_file_wave_object.readframes(frames_to_read)

    print("End of file")
    my_stream.close_stream()


def player_audio_array(audio_array, rate):
    MAX_INTEGER = 32768.0
    BUFFER_SIZE = int(1024)
    print(f"Framerate: {rate} samples/sec")

    # filtrage item
    my_rt_filter = rt_filtering.Audio_filter_rt(rate, BUFFER_SIZE)
    my_rt_filter.set_bandpass(lowcut=150, highcut=2500, order=4)
    # my_rt_filter.set_highpass(fcut=2000, order=2)
    my_rt_filter.init_rt_filtering()

    # my_rt_filter.audio_filter.computeFilterFreqResp()
    # my_rt_filter.audio_filter.plotFilterResponse()

    # plotting definition
    visualizer = ricanelib.Spectrum_vizualier(memory_size=my_rt_filter.memory_size,
                                              buffer_size=my_rt_filter.buffer_size)

    print("open stream")
    my_stream = audiostream.AudioStream(n_channels=1,
                                        stream_rate=rate,
                                        buffer_size=BUFFER_SIZE)
    my_stream.init_array_stream()

    # define player
    player = ricanelib.PlayerRecorder()
    player.load_audio_array_as_content(audio_array, rate, BUFFER_SIZE, MAX_INTEGER)

    while player.input_file_bytes != b'':
        my_rt_filter.buffer_data = droulib.bufferBytesToData(player.input_file_bytes, MAX_INTEGER)
      
        if len(my_rt_filter.buffer_data) != my_rt_filter.buffer_size:
            # zero padding du pauvre
            size_missing = int((my_rt_filter.buffer_size - len(my_rt_filter.buffer_data)) / 2)
            my_rt_filter.buffer_data = np.pad(my_rt_filter.buffer_data, size_missing).tolist()
        if len(my_rt_filter.memory_data) != my_rt_filter.buffer_size * my_rt_filter.memory_size:
            # zero padding du pauvre
            size_missing = int((my_rt_filter.buffer_size * my_rt_filter.memory_size - len(my_rt_filter.memory_data)) / 2)
            my_rt_filter.memory_data = np.pad(my_rt_filter.memory_data, size_missing).tolist()
   
        # -- POSSIBLE DSP ON INPUT_FILE_FRAME --
        # my_rt_filter.filter_buffer_data()
        my_rt_filter.feedforward(delay=64)
        # -- END OF DSP --
        my_rt_filter.save_in_memory()
        # playback filtered chunk
        my_stream.populate_playback(droulib.bufferDataToBytes(my_rt_filter.buffer_data, MAX_INTEGER))

        # plotting
        # visualizer.populate_plot(data_line=my_rt_filter.buffer_data, data_line2=my_rt_filter.memory_data)
        # load new chunk
        player.read_frames()

    print("End of file")
    my_stream.close_stream()

# define callback (2)
def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)


def io_filtering(rate):
    MAX_INTEGER = 32768.0
    BUFFER_SIZE = 1024
    print("open stream")
    my_stream = audiostream.AudioStream()
    my_stream.update_buffer_size(BUFFER_SIZE)
    my_stream.update_n_channels(1)
    my_stream.update_stream_rate(rate)

    # filtrage item
    my_rt_filter = rt_filtering.Audio_filter_rt(rate, BUFFER_SIZE)
    # my_rt_filter.set_bandpass()
    my_rt_filter.set_highpass()
    my_rt_filter.init_rt_filtering()

    print(f"Framerate: {rate} samples/sec")
    my_stream.init_new_stream()
 
    frames_to_read = int(BUFFER_SIZE/1)
    print("On Air")
    input_file_bytes = my_stream.stream.read(frames_to_read)
    while input_file_bytes != b'':
        my_rt_filter.buffer_data = droulib.bufferBytesToData(input_file_bytes, MAX_INTEGER)
        # -- POSSIBLE DSP ON INPUT_FILE_FRAME --
        my_rt_filter.filter_buffer_data()
        # -- END OF DSP --
        my_stream.populate_playback(droulib.bufferDataToBytes(my_rt_filter.buffer_data, MAX_INTEGER))
        input_file_bytes = my_stream.stream.read(frames_to_read)

    print("End of file")
    my_stream.close_stream()

if __name__ == "__main__":
    # Global Parameters
    sweep, tsweep = audiogenerator.generateSweptSine(amp=0.5,
                                                     f0=150,
                                                     f1=10000,
                                                     duration=1.0,
                                                     fs=config.SAMPLING_FREQUENCY,
                                                     fade=True,
                                                     novak=True)
    
    play_from_audio_array(sweep, config.SAMPLING_FREQUENCY)
    # load audio as wave_read object
    # read_filepath = config.AUDIO_FILE_TEST
    # play_file_from_filepath(read_filepath)
    # io_filtering(44100)

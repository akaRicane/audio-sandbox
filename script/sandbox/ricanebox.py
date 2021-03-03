import os
import sys
import wave
import droulib
import numpy as np
import matplotlib.pyplot as plt
from tkinter import TclError
import time
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
    my_rt_filter.set_bandpass(lowcut=600, highcut=6500, order=4)
    # my_rt_filter.set_highpass(fcut=2000, order=2)
    my_rt_filter.init_rt_filtering()

    # my_rt_filter.audio_filter.computeFilterFreqResp()
    # my_rt_filter.audio_filter.plotFilterResponse()

    # plotting definition
    x2_max = BUFFER_SIZE * my_rt_filter.memory_size
    fig, (ax, ax2) = plt.subplots(2, figsize=(15, 8))
    x = np.arange(0, BUFFER_SIZE)
    # x2 = np.arange(0, x2_max)

    line, = ax.plot(x, np.random.rand(BUFFER_SIZE), '-', lw=2)
    # line2, = ax2.plot(x2, np.random.rand(x2_max), '-', lw=2)

    ax.set_title("AUDIO WAVEFORM")
    ax.set_xlabel("Samples")
    ax.set_ylabel("Magnitude")
    ax.set_xlim(0, BUFFER_SIZE)
    ax.set_ylim(-1, 1)
    plt.setp(ax, xticks=[0, int(BUFFER_SIZE / 2), BUFFER_SIZE], yticks=[-1, 1])

    # ax2.set_title("MEMORY")
    # ax2.set_xlabel("Full signal memory")
    # ax2.set_ylabel("Mangitude")
    # ax2.set_xlim(0, x2_max)
    # ax2.set_ylim(-1, 1)
    # plt.setp(ax2, xticks=[0, int(x2_max / 2), x2_max], yticks=[-1, 1])
    plt.show(block=False)
    line.set_ydata(my_rt_filter.buffer_data)
    # line2.set_ydata(my_rt_filter.memory_data)
    ...
    print("open stream")
    my_stream = audiostream.AudioStream()
    my_stream.update_buffer_size(BUFFER_SIZE)
    my_stream.update_n_channels(1)
    my_stream.update_stream_rate(rate)

    my_stream.init_new_stream()
    input_file_wave_object = droulib.convertMonoDatatoWaveObject(audio_array,
                                                                 rate,
                                                                 'test.wav',
                                                                 MAX_INTEGER)
    frame_count = 0
    start_time = time.time()
    frames_to_read = int(BUFFER_SIZE/input_file_wave_object.getnchannels())
    input_file_bytes = input_file_wave_object.readframes(frames_to_read)

    while input_file_bytes != b'':
        my_rt_filter.buffer_data = droulib.bufferBytesToData(input_file_bytes, MAX_INTEGER)

        # -- POSSIBLE DSP ON INPUT_FILE_FRAME --
        my_rt_filter.filter_buffer_data()
        # -- END OF DSP --
        my_rt_filter.save_in_memory()

        # playback filtered chunk
        my_stream.populate_playback(droulib.bufferDataToBytes(my_rt_filter.buffer_data, MAX_INTEGER))

        if len(my_rt_filter.buffer_data) != my_rt_filter.buffer_size:
            # zero padding du pauvre
            size_missing = float(my_rt_filter.buffer_size) - len(my_rt_filter.buffer_data)
            my_rt_filter.buffer_data = np.pad(my_rt_filter.buffer_data, int(size_missing)).tolist()
        # plotting
        line.set_ydata(my_rt_filter.buffer_data)
        # line2.set_ydata(my_rt_filter.memory_data)
        try:
            fig.canvas.draw()
            fig.canvas.flush_events()
            frame_count += 1
        except:
            frame_rate = frame_count / (time.time() - start_time)
            print("Stream is stopped")
            print(f"Average frame rate: {frame_rate}")
        # load new chunk
        input_file_bytes = input_file_wave_object.readframes(frames_to_read)

    print("End of file")
    my_stream.close_stream()


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
                                                     duration=2.0,
                                                     fs=config.SAMPLING_FREQUENCY,
                                                     fade=True,
                                                     novak=True)
    
    play_from_audio_array(sweep, config.SAMPLING_FREQUENCY)
    # load audio as wave_read object
    # read_filepath = config.AUDIO_FILE_TEST
    # play_file_from_filepath(read_filepath)
    # io_filtering(44100)
    ...

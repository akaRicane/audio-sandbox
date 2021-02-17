import pyaudio
import os, sys
import wave
import matplotlib.pyplot as plt
import numpy as np
import struct
from scipy.fftpack import fft
import time
from tkinter import TclError
from scipy.io import wavfile

sys.path.append(os.getcwd())
from lib import config, tool, audiodsp


# Import test file
filename_player = os.path.join('inputs','CSC_sweep_20-20k.wav')
file_player = wave.open(filename_player, 'rb')
# the file name output you want to record into
filename_record = os.path.join('inputs','recording.wav')

# initialize PyAudio object
p = pyaudio.PyAudio()

# set the chunk size of 1024 samples
CHUNK = 2**(10+1)
# sample format
FORMAT = p.get_format_from_width(file_player.getsampwidth())
sample_format_recorder = pyaudio.paInt16
# mono, change to 2 if you want stereo
CHANNEL = file_player.getnchannels()
# 44100 samples per second
RATE = file_player.getframerate()

# open stream object as input & output
stream = p.open(format=FORMAT,
                channels=CHANNEL,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

# Read data in chunks
data_player = file_player.readframes(CHUNK)

frames = []  # Initialize array to store frames

# Play the sound by writing the audio data to the stream
while data_player != b'':
    stream.write(data_player)
    data_recorder = stream.read(CHUNK)
    data_player = file_player.readframes(CHUNK)
    frames.append(data_recorder)
# Stop, Close and terminate the stream
stream.stop_stream()
stream.close()
p.terminate()

print('-----Finished Recording-----')
# Open and Set the data of the WAV file
file_recorder = wave.open(filename_record, 'wb')
file_recorder.setnchannels(CHANNEL)
file_recorder.setsampwidth(p.get_sample_size(sample_format_recorder))
file_recorder.setframerate(RATE)
 
#Write and Close the File
file_recorder.writeframes(b''.join(frames))
file_recorder.close()
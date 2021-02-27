import pyaudio
import os, sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import wave
import struct
from scipy.io import wavfile
from scipy.fftpack import fft, fftfreq
import droulib

sys.path.append(os.getcwd())
from lib import audiogenerator, audiodsp, tool

# Global Parameters
BUFFER_SIZE = 1024*2
SAMPLE_RATE = 48000
MAX_INT = 32768.0

# Generate signal
sweep, tsweep = audiogenerator.generateSweptSine(amp=0.5,
                                                 f0=20,
                                                 f1=20000,
                                                 duration=2.5,
                                                 fs=SAMPLE_RATE,
                                                 fade=True,
                                                 novak=True)

# Convert signal to waveread object
filename = os.path.join('resources','Sweep.wav')
inPut = droulib.convertMonoDatatoWaveObject(sweep, SAMPLE_RATE, filename, MAX_INT)

# Define filter
coefs = signal.butter(2, [40, 18000] , btype='bandpass', analog=False, fs=SAMPLE_RATE, output='sos')
# Play and filtrer function
droulib.filterAndPlay(inPut, coefs, SAMPLE_RATE, BUFFER_SIZE, MAX_INT, plot=True, mute=True)


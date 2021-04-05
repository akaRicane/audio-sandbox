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

filename_player = os.path.join('inputs','CSC_sweep_20-20k.wav')
filename_record = os.path.join('inputs','recording.wav')

rate_in, data_in = wavfile.read(filename_player)
rate_out, data_out = wavfile.read(filename_record)

t_in = audiodsp.getTemporalVector(data_in,rate_in)
t_out = audiodsp.getTemporalVector(data_out,rate_out)


fft_in = fft(data_in, n=480000)
fft_out = fft(data_out, n=480000)
fft_TF = fft_out/fft_in

TF_amp, TF_phase = audiodsp.splitFftVector(fft_TF)

f_in = audiodsp.getFrequencyVector(fft_in, rate_in)
f_out = audiodsp.getFrequencyVector(fft_out, rate_out)

plt.figure(1)
plt.subplot(211)
plt.plot(t_in, data_in)
plt.plot(t_out, data_out)
plt.subplot(212)
plt.semilogx(f_in, 20*np.log10(abs(fft_in[0:int(len(fft_in)/2)])))
plt.semilogx(f_out, 20*np.log10(abs(fft_out[0:int(len(fft_out)/2)])))

plt.figure(2)
plt.subplot(211)
plt.semilogx(f_in, 20*np.log10(abs(TF_amp[0:int(len(fft_in)/2)])))
plt.subplot(212)
plt.semilogx(f_in, TF_phase[0:int(len(fft_in)/2)])
plt.show()
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

# Initialize empty array to stock buffers
frames_in=[]
frames_out=[]

# Generate signal
sweep, tsweep = audiogenerator.generateSweptSine(amp=0.1,
                                                 f0=20,
                                                 f1=20000,
                                                 duration=5,
                                                 fs=SAMPLE_RATE,
                                                 fade=True,
                                                 novak=True)
                                                 
# Convert signal to waveread object
filename = os.path.join('resources','Sweep.wav')
inPut = droulib.convertMonoDatatoBytes(sweep, SAMPLE_RATE, filename, MAX_INT)

# Define filter
coefs = signal.butter(2, 500 , btype='high', analog=False, fs=SAMPLE_RATE, output='sos')
# Play and filtrer function
in_data, out_data = droulib.playAndFilter(inPut, coefs, SAMPLE_RATE, BUFFER_SIZE, MAX_INT)

################### plot part #######################
fft_in = fft(in_data)
f = fftfreq(len(fft_in), d=1/SAMPLE_RATE)
fft_in = audiodsp.retCleanFft(fft_in)
fft_out = fft(out_data)
fft_out = audiodsp.retCleanFft(fft_out)
f = audiodsp.retCleanFft(f)

plt.figure(1)
plt.subplot(311)
plt.plot(audiodsp.getTemporalVector(in_data,SAMPLE_RATE), in_data)
plt.plot(audiodsp.getTemporalVector(out_data,SAMPLE_RATE), out_data)
plt.grid()
plt.subplot(312)
plt.semilogx(f,20*np.log10(abs(np.array(fft_in))))
plt.semilogx(f,20*np.log10(abs(np.array(fft_out))))
plt.xlim(10,20000)
plt.ylim(-10,70)
plt.grid()
plt.subplot(313)
plt.semilogx(f, 20*np.log10(abs(np.array(fft_out)/np.array(fft_in))))
plt.xlim(10,20000)
plt.ylim(-40,40)
plt.grid()
plt.show()

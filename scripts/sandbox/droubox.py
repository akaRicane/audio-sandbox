import pyaudio
import os, sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import wave
import struct
from scipy.io import wavfile
from scipy.fftpack import fft, fftfreq
import droulib, audiostream
from scipy.signal import savgol_filter

sys.path.append(os.getcwd())
from lib import audiogenerator, audiodsp, tool

# Global Parameters
BUFFER_SIZE = int(1024/4)
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
# coefs = signal.butter(2, 1000 , btype='bandpass', analog=False, fs=SAMPLE_RATE, output='sos')
# coefs = signal.butter(6, [3000, 6000] , btype='bandpass', analog=False, fs=SAMPLE_RATE, output='sos')
coefs = droulib.parametriqEQ(gain=10**((-24)/20), f0=1000, bandWidth=SAMPLE_RATE, rate=SAMPLE_RATE, output='sos')


# Play and filtrer function
# droulib.filterAndPlay(inPut, coefs, SAMPLE_RATE, BUFFER_SIZE, MAX_INT, plot=True, mute=False)
signal, filt_signal = droulib.RecordAndFilter(recordTime=10, nChannels=1, filterCoefs=coefs, rate=SAMPLE_RATE, bufferSize=BUFFER_SIZE, maximumInteger=MAX_INT, playback=True)
t = audiodsp.getTemporalVector(filt_signal, SAMPLE_RATE)

fft_in = fft(signal)
fft_out = fft(filt_signal)
f = fftfreq(len(fft_in), d=1/SAMPLE_RATE)

TF = savgol_filter(abs(fft_out[0:int(len(f)/2)]/fft_in[0:int(len(f)/2)]), 51, 3)


plt.figure(1)
plt.subplot(211)
plt.plot(t, signal)
plt.plot(t, filt_signal)
plt.grid()
plt.subplot(212)
plt.semilogx(f[0:int(len(f)/2)], 20*np.log10(abs(fft_in[0:int(len(f)/2)])))
plt.semilogx(f[0:int(len(f)/2)], 20*np.log10(abs(fft_out[0:int(len(f)/2)])))
plt.semilogx(f[0:int(len(f)/2)], 20*np.log10(abs(TF)))
plt.xlim(20, 20000)
plt.grid()
plt.show()

############################## EQ Test ##########################################
# b, a = droulib.parametriqEQ(gain=10**(6/20), f0=100, bandWidth=SAMPLE_RATE, rate=SAMPLE_RATE)
# coefs2 = signal.tf2sos(b, a)
# b, a = droulib.parametriqEQ(gain=10**(-3/20), f0=350, bandWidth=SAMPLE_RATE, rate=SAMPLE_RATE)
# coefs3 = signal.tf2sos(b, a)
# b, a = droulib.parametriqEQ(gain=10**(3/20), f0=1000, bandWidth=SAMPLE_RATE, rate=SAMPLE_RATE)
# coefs4 = signal.tf2sos(b, a)
# b, a = droulib.parametriqEQ(gain=10**(6/20), f0=3500, bandWidth=SAMPLE_RATE, rate=SAMPLE_RATE)
# coefs5 = signal.tf2sos(b, a)
# b, a = droulib.parametriqEQ(gain=10**(-2/20), f0=10000, bandWidth=SAMPLE_RATE, rate=SAMPLE_RATE)
# coefs6 = signal.tf2sos(b, a)
# b, a = droulib.parametriqEQ(gain=10**(6/20), f0=18000, bandWidth=SAMPLE_RATE, rate=SAMPLE_RATE)
# coefs7 = signal.tf2sos(b, a)
# fft1 = fft(sweep)
# freq = fftfreq(len(fft1), d=1/SAMPLE_RATE)

# sweep1 = signal.sosfilt(coefs, sweep)
# sweep2 = signal.sosfilt(coefs2, sweep1)
# sweep3 = signal.sosfilt(coefs3, sweep2)
# sweep4 = signal.sosfilt(coefs4, sweep3)
# sweep5 = signal.sosfilt(coefs5, sweep4)
# sweep6 = signal.sosfilt(coefs6, sweep5)
# sweep7 = signal.sosfilt(coefs7, sweep6)

# fft2 = fft(sweep7)

# plt.figure(1)
# plt.semilogx(freq[0:int(len(freq)/2)], 20*np.log10(abs(fft1[0:int(len(fft1)/2)])))
# plt.semilogx(freq[0:int(len(freq)/2)], 20*np.log10(abs(fft2[0:int(len(fft2)/2)])))
# plt.xlim(10, 22000)
# plt.ylim(20, 70)
# plt.grid()
# plt.show()
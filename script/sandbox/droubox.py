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
SAMPLE_RATE = 44100
MAX_INT = 32768.0

# Initialize empty array to stock buffers
frames_in=[]
frames_out=[]

# Generate signal
sweep, tsweep = audiogenerator.generateSweptSine(amp=0.9, f0=20, f1=20000, duration=2.5, fs=SAMPLE_RATE, fade=True, novak=True)

# Convert signal to waveread object
filename = os.path.join('resources','Sweep.wav')
inPut = droulib.convertMonoDatatoBytes(sweep, SAMPLE_RATE, filename, MAX_INT)

# Get number of channels
nChannels = inPut.getnchannels()

# Initialize player
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=nChannels,
                rate=SAMPLE_RATE,
                input=False,
                output=True,
                frames_per_buffer=BUFFER_SIZE)

# Define filter
coefs = signal.butter(2, 500 , btype='high', analog=False, fs=SAMPLE_RATE, output='sos')
# Initialize first buffer filter (updating with loop iterations)
filter_buffer = signal.sosfilt_zi(coefs)
# Read first data buffer
data = inPut.readframes(int(BUFFER_SIZE/nChannels))

# Filtering and playing loop
while data != b'':
    # read audio
    bytes_audio_data_in = data
    # convert buffer into array of buffer size for filtering
    audio_data_in = droulib.bufferBytesToData(bytes_audio_data_in, MAX_INT)
    # Filter buffer array
    audio_data_out, filter_buffer = signal.sosfilt(coefs, audio_data_in, zi=filter_buffer)
    # Convert back filtered buffer array into readable object buffer
    string_audio_data_out = droulib.bufferDataToBytes(audio_data_out, MAX_INT)
    # Play audio on output
    # stream.write(bytes_audio_data_out, BUFFER_SIZE)
    # next data
    data = inPut.readframes(int(BUFFER_SIZE/nChannels))
    # append input and filtered buffers for plot and/or export
    frames_out.append(audio_data_out)
    frames_in.append(audio_data_in)

# Close stream and open objects
stream.stop_stream()
stream.close()
inPut.close()
p.terminate()

################### plot part #######################
in_data = np.concatenate(frames_in)
out_data = np.concatenate(frames_out)
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

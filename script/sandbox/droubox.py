import pyaudio
import os, sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import wave
import struct
from scipy.io import wavfile
from scipy.fftpack import fft, fftfreq

sys.path.append(os.getcwd())
from lib import audiogenerator, audiodsp, tool

BUFFER_SIZE = 1024*2
SAMPLE_RATE = 44100
MAX_INT = 32768.0

sweep, tsweep = audiogenerator.generateSweptSine(amp=0.9, f0=20, f1=20000, duration=2.5, fs=SAMPLE_RATE, fade=True, novak=True)
sweep_stream = sweep.astype(np.float32).tobytes()
obj = wave.open('sound.wav','w')
obj.setnchannels(1) # mono
obj.setsampwidth(2)
obj.setframerate(SAMPLE_RATE)
for i, value in enumerate(sweep):
   data = struct.pack('<h', int(value*32767))
   obj.writeframesraw( data )
obj.close()
inPut = wave.open('sound.wav','r')
p = pyaudio.PyAudio()

stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=SAMPLE_RATE,
    input=False,
    output=True,
    frames_per_buffer=BUFFER_SIZE
)

filename = os.path.join('resources','gaussian_white_noise.wav')
wf = wave.open(filename, 'rb')
nChannels = wf.getnchannels()

audio_data_out = np.ndarray(shape=(BUFFER_SIZE,1), dtype=np.float64)

b, a = signal.butter(1, [2000, 10000] , btype='bandstop', analog=False, fs=SAMPLE_RATE)
filter_buffer = signal.lfilter_zi(b, a)
frames_in=[]
frames_out=[]
data = inPut.readframes(int(BUFFER_SIZE/nChannels))
# data = np.frombuffer(data, dtype=np.int16) / MAX_INT
# data, filter_buffer = signal.lfilter(b, a, data, zi=filter_buffer)
# data = np.array(np.round_(data * MAX_INT), dtype=np.int16).tobytes()
while data != b'':
    # read audio
    string_audio_data_in = data
    audio_data_in = np.frombuffer(string_audio_data_in, dtype=np.int16) / MAX_INT
    audio_data_out, filter_buffer = signal.lfilter(b, a, audio_data_in, zi=filter_buffer)

    # write audio
    string_audio_data_out = np.array(np.round_(audio_data_out * MAX_INT), dtype=np.int16).tobytes()
    stream.write(string_audio_data_out, BUFFER_SIZE)
    # next data
    data = inPut.readframes(int(BUFFER_SIZE/nChannels))
    # append for plot and/or export
    frames_out.append(audio_data_out)
    frames_in.append(audio_data_in)

stream.stop_stream()
stream.close()
p.terminate()


in_data = np.concatenate((frames_in))
out_data = np.concatenate((frames_out))
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
plt.semilogx(f,tool.convertAmpToAmpDb(fft_in))
plt.semilogx(f,tool.convertAmpToAmpDb(fft_out))
plt.xlim(10,20000)
plt.ylim(-10,70)
plt.grid()
plt.subplot(313)
plt.semilogx(f, tool.convertAmpToAmpDb(np.array(fft_out)/np.array(fft_in)))
plt.xlim(10,20000)
plt.ylim(-40,40)
plt.grid()
plt.show()

import pyaudio
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import wave

BUFFER_SIZE = 1024*4
SAMPLE_RATE = 44100
MAX_INT = 32768.0


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

iir_buffer = [0.0, 0.0]
#a = [1, -1.7469, 0.7755]
#b = [0.9168, -1.7598, 0.8458]
b, a = signal.butter(2, 100/SAMPLE_RATE*2, analog=False)
frames_in=[]
frames_out=[]
data = wf.readframes(int(BUFFER_SIZE/nChannels))
while data != b'':
    # read audio
    string_audio_data_in = data
    audio_data_in = np.frombuffer(string_audio_data_in, dtype=np.int16) / MAX_INT
    # filtering quite strange way
    for i, sample_in in enumerate(audio_data_in):
        temp = sample_in - a[1]*iir_buffer[1] - a[2]*iir_buffer[0]
        audio_data_out[i] = b[0]*temp + b[1]*iir_buffer[1] + b[2]*iir_buffer[0]
        iir_buffer[0] = iir_buffer[1]
        iir_buffer[1] = temp

    # write audio
    string_audio_data_out = np.array(np.round_(audio_data_out * MAX_INT), dtype=np.int16).tobytes()
    stream.write(string_audio_data_out, BUFFER_SIZE)
    frames_out.append(audio_data_out)
    frames_in.append(audio_data_in)
    # next data
    data = wf.readframes(int(BUFFER_SIZE/nChannels))

stream.stop_stream()
stream.close()
p.terminate()
print(np.concatenate(np.concatenate((frames_out))))
print(np.concatenate(frames_in))
plt.figure(1)
plt.plot(np.concatenate((frames_in)))
plt.plot(np.concatenate(np.concatenate((frames_out))))
plt.show()
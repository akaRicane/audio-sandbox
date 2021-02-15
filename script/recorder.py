import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np
import struct
from scipy.fftpack import fft
import time
from tkinter import TclError
from scipy.io import wavfile

# the file name output you want to record into
filename = "recording.wav"
# set the chunk size of 1024 samples
CHUNK = 1024*(2**3)
# sample format
FORMAT = pyaudio.paInt16
# mono, change to 2 if you want stereo
CHANNEL = 1
# 44100 samples per second
RATE = 44100
record_seconds = 5
# if you want playback on recording
playback = False
# if you want audio to be plotted
rec_plot = False

fig, (ax) = plt.subplots(1, figsize=(15, 8))
x = np.arange(0, 2 * CHUNK, 2)
line, = ax.plot(x, np.random.rand(CHUNK), '-', lw=2)
ax.set_title("AUDIO WAVEFORM")
ax.set_xlabel("samples")
ax.set_ylabel("volume")
# ax.set_xlim(0, 2 * CHUNK)
ax.set_ylim(0, 255)
#plt.setp(ax, xticks=[0, CHUNK, 2 * CHUNK], yticks=[0, 120, 255])
if rec_plot == True:
    plt.show(block=False)

# initialize PyAudio object
p = pyaudio.PyAudio()
# open stream object as input & output
stream = p.open(format=FORMAT,
                channels=CHANNEL,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)


frames = []
frame_count = 0
print("Recording...")
for i in range(int(44100 / CHUNK * record_seconds)):
    # Recording
    data = stream.read(CHUNK)
    # Playback
    if playback == True:# Playback
        stream.write(data)
    frames.append(data)
    if rec_plot == True:
        data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
        data_np = np.array(data_int, dtype='b')[::2] + 128
        line.set_ydata(data_np)
        try:
            fig.canvas.draw()
            fig.canvas.flush_events()
            frame_count += 1
        except TclError:
            frame_rate = frame_count / (time.time() - start_time)
            print("Stream is stopped")
            print(f"Average frame rate: {frame_rate}")
            break

print("Finished recording.")
# stop and close stream
stream.stop_stream()
stream.close()
# terminate pyaudio object
p.terminate()
# save audio file
# open the file in 'write bytes' mode
wf = wave.open(filename, "wb")
# set the channels
wf.setnchannels(CHANNEL)
# set the sample format
wf.setsampwidth(p.get_sample_size(FORMAT))
# set the sample rate
wf.setframerate(RATE)
# write the frames as bytes
wf.writeframes(b"".join(frames))
# close the file
wf.close()

rate, data = wavfile.read("recording.wav")

plt.cla()
x = np.arange(0, len(data), 1)
plt.subplot(211)
plt.plot(x/rate, data, '-', lw=1, color='blue')
plt.grid()
plt.subplot(212)
x_fft = np.linspace(0, rate, len(data))
y_fft = abs(fft(data))
plt.semilogx(x_fft, 20*np.log10(y_fft), '-', lw=1, color='red')
plt.xlim(20, 20000)
plt.grid()
plt.show()
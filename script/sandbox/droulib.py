import wave, struct
import pyaudio
import os, sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fftpack import fft, fftfreq

sys.path.append(os.getcwd())
from lib import audiogenerator, audiodsp


def convertMonoDatatoWaveObject(data, rate, filename, maximumInteger):
    """ Convert synthetic signal x to bytes object readable by readframes function of wave module
    Args:
        [list]:     data,          signal data
        [int]:      rate,       sampling frequency of the signal
        [string]:   filename,   name of the wavfile that will be created
    Returns:
        [class: waveread object]:      bytesData
    """
    obj = wave.open(filename,'w')
    obj.setnchannels(1) # mono
    obj.setsampwidth(2)
    obj.setframerate(rate)
    for value in data:
        _bytesdata = struct.pack('<h', int(value*maximumInteger))
        obj.writeframesraw(_bytesdata)
    obj.close()
    bytesData = wave.open(filename,'r')
    return bytesData


def convertWaveobjectToData(waveobject, maximumInteger):
    # Read file to get buffer
    samples = waveobject.getnframes()
    audio = waveobject.readframes(samples)
    # Convert buffer to float32 with numPy
    audio_int16 = np.frombuffer(audio, dtype=np.int16)
    data = audio_int16.astype(np.float)/maximumInteger
    return data


def bufferBytesToData(bytesData, maximumInteger):
    data = np.frombuffer(bytesData, dtype=np.int16) / maximumInteger
    return data


def bufferDataToBytes(data, maximumInteger):
    bytesData = np.array(np.round_(data*maximumInteger), dtype=np.int16).tobytes()
    return bytesData


def filterAndPlay(wavinput, filterCoefs, rate, bufferSize, maximumInteger, plot=False):
    frames_in=[]
    frames_out=[]
    # Get number of channels
    nChannels = wavinput.getnchannels()
    # Initialize player
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=nChannels,
                    rate=rate,
                    input=False,
                    output=True,
                    frames_per_buffer=bufferSize)
    # Read first data buffer
    data = wavinput.readframes(int(bufferSize/nChannels))
    # Initialize first buffer filter (updating with loop iterations)
    filter_buffer = signal.sosfilt_zi(filterCoefs)
    # Filtering and playing loop
    while data != b'':
        # read audio
        bytes_audio_data_in = data
        # convert buffer into array of buffer size for filtering
        audio_data_in = bufferBytesToData(bytes_audio_data_in, maximumInteger)
        # Filter buffer array
        audio_data_out, filter_buffer = signal.sosfilt(filterCoefs, audio_data_in, zi=filter_buffer)
        # Convert back filtered buffer array into readable object buffer
        bytes_audio_data_out = bufferDataToBytes(audio_data_out, maximumInteger)
        # Play audio on output
        stream.write(bytes_audio_data_out, bufferSize)
        # next data
        data = wavinput.readframes(int(bufferSize/nChannels))
        # append input and filtered buffers for plot and/or export
        frames_out.append(audio_data_out)
        frames_in.append(audio_data_in)
    # Concatenate each buffer arrays into a single data array
    dataIn = np.concatenate(frames_in)
    dataOut = np.concatenate(frames_out)
    # Close stream and open objects
    stream.stop_stream()
    stream.close()
    wavinput.close()
    p.terminate()
    if plot == True:
        fft_in = fft(dataIn)
        f = fftfreq(len(fft_in), d=1/rate)
        fft_in = audiodsp.retCleanFft(fft_in)
        fft_out = fft(dataOut)
        fft_out = audiodsp.retCleanFft(fft_out)
        f = audiodsp.retCleanFft(f)
        plt.figure(1)
        plt.subplot(311)
        plt.plot(audiodsp.getTemporalVector(dataIn,rate), dataIn)
        plt.plot(audiodsp.getTemporalVector(dataOut,rate), dataOut)
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
        plt.ylim(-15,15)
        plt.grid()
        plt.show()


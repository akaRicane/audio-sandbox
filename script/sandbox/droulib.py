import wave, struct
import pyaudio
import os, sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
sys.path.append(os.getcwd())
from lib import audiogenerator

def convertMonoDatatoBytes(x, rate, filename, maximumInteger):
    """ Convert synthetic signal x to bytes object readable by readframes function of wave module
    Args:
        [list]:     x,          signal data
        [int]:      rate,       sampling frequency of the signal
        [string]:   filename,   name of the wavfile that will be created
    Returns:
        [class: waveread object]:      bytesData
    """
    obj = wave.open(filename,'w')
    obj.setnchannels(1) # mono
    obj.setsampwidth(2)
    obj.setframerate(rate)
    for i, value in enumerate(x):
        data = struct.pack('<h', int(value*maximumInteger))
        obj.writeframesraw( data )
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


def playAndFilter(wavinput, filterCoefs, rate, bufferSize, maximumInteger):
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
    return dataIn, dataOut




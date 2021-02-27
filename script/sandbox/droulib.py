import wave, struct
import os, sys
import numpy as np
import matplotlib.pyplot as plt

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


SAMPLE_RATE = 44100
MAX_INT = 32768.0
filename = os.path.join('resources','Sweep.wav')
sweep, tsweep = audiogenerator.generateSweptSine(amp=0.9, f0=20, f1=20000, duration=2.5, fs=SAMPLE_RATE, fade=True, novak=True)
bytesSweep = convertMonoDatatoBytes(sweep, SAMPLE_RATE, filename, MAX_INT)
dataSweep = convertWaveobjectToData(bytesSweep, MAX_INT)


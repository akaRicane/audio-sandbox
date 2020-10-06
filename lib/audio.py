import os
import sys
import copy
from pathlib import Path

from lib import audiodsp, audiofile, audioplot, audiogenerator
from lib import config

class AudioItem():
    def __init__(self):
        # Common parameters of AudioItem
        self.nchannel = 0
        self.codec = None
        self.data = []
    
    # Channel Management
    def addChannel(self):
        self.data.append(AudioData())  # TODO add new audioDataItem
        self.nchannel = len(self.data)

    def deleteChannel(self, indexToDelete):
        del self.data[indexToDelete]
        self.nchannel = len(self.data)
        
    def cloneChannel(self, indexToClone):
        self.addChannel()
        self.data[-1] = copy.deepcopy(self.data[indexToClone])

    def makeStereo(self):
        self.cloneChannel(indexToClone=0)

    def setAudioItemToMono(self, indexToKeep=0):
        self.data[0] = copy.deepcopy(self.data[indexToKeep])
        for idx, _ in enumerate(self.data):
            if idx != 0:
                self.deleteChannel(idx)
    
    def addSinusAsNewChannel(self):
        self.addChannel()
        self.data[-1].loadSinus()
            

class AudioData():
    def __init__(self):
        self.npts = None
        self.rate = config.SAMPLING_FREQUENCY
        self.t = None
        self.tamp = None
        self.f = None
        self.famp = None
        self.ffampDb = None
        self.fphase = None
        self.temporalAvailable = False
        self.spectralAvailable = False
    
    # Data Management    
    def setTemporalContent(self, timeVector: list, amplitude: list):
        self.tamp = amplitude
        self.t = timeVector
        self.npts = len(self.t)
        self.temporalAvailable = True
    
    def setSpectralContent(self, freq: list, amplitude: list, amplitude_db: list=None, phase: list=None):
        self.f = freq
        self.famp = amplitude
        self.fampDb = amplitude_db
        self.fphase = phase
        self.spectralAvailable = True
    
    def loadSinus(self, f=1000, A=1):
        self.rate = config.SAMPLING_FREQUENCY
        self.setTemporalContent(*audiogenerator.generateSine(f=f, A=A))

    def loadAudioFile(self):
        self.rate, self.amp, self.codec = audiofile.read(config.AUDIO_FILE_TEST)
        self.t = audiodsp.getTemporalVector(self.tamp, fs=self.rate)
    
    def getfft(self, iscomplex=False):
        self.setSpectralContent(audiodsp.getFft(t=self.t, tamp=self.tamp, fs=self.rate, N=config.FFT_WINDOWING))
    
    def plot(self, space="time", mode="short", show=False):
        if mode == "short":
            if space == "time":
                audioplot.shortPlot(self.t, self.tamp, space="time")
            elif space == "spectral":
                audioplot.shortPlot(self.f, self.fampDb, space="spectral")
        else:
            logging.error("Plot not possible")
        if show:
            audioplot.pshow() 

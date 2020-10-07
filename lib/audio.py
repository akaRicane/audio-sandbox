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
        self.data.append(AudioData())
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
        self.fphase = None
        self.temporalAvailable = False
        self.spectralAvailable = False
        self.info = {
            "SNR": '96 dB',
            'THD': '0.001%'
        }
    
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
    
    def fft(self, iscomplex=False):
        self.setSpectralContent(*audiodsp.getFft(t=self.t, tAmplitude=self.tamp, fs=self.rate))
    
    def plot(self, space="time", mode="short", show=False):
        legendList = []
        if mode == "short":
            if space == "time":
                audioplot.shortPlot(self.t, self.tamp, space=space)
                legendList.append("Time Plot")
            elif space == "spectral":
                audioplot.shortPlot(self.f, self.fampDb, space=space)
                legendList.append("Spectral Plot")
        else:
            logging.error("Plot not possible")
        if show:
            audioplot.pshow(legend=legendList)

    def callBoardControl(self):
        vect = [self.t, self.f]
        data = [[self.tamp], [self.fampDb]]
        audioplot.boardControl(vect=vect, data=data, additionalData=self.info, legendList=["temporal", "spectral", "spectral2"])

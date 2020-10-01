import os
import sys
from pathlib import Path

from lib import audiodsp, audiofile, audioplot, audiogenerator
from lib import config

class AudioItem():
    def __init__(self):
        name = None
        temporalAvailable = False
        spectralAvailable = False
        rate = config.SAMPLING_FREQUENCY
        nchannel = None
        npts = None
        codec = None
        t = None
        tamp = None
        f = None
        famp = None
        ffampDb = None
    def setToMono(self):
        if self.temporalAvailable:
            self.tamp = audiodsp.toMono(self.tamp)
        elif self.spectralAvailable:
            self.famp = audiodsp.toMono(self.famp)
            self.fampDb = audiodsp.toMono(self.fampDb)

    def setTemporalContent(self, t, tamp):
        self.t = t
        self.tamp = tamp
        self.temporalAvailable =  True
    
    def setSpectralContent(self, f, famp, fampDb):
        self.f = f
        self.famp = famp
        self.fampDb = fampDb
        self.spectralAvailable = True
    
    def loadSinus(self, f=1000, A=0.5):
        self.t, self.tamp = audiogenerator.generateSine(f=f, A=A)
        self.temporalAvailable = True
        self.npts = len(self.t)
        self.nchannel = 1
        self.name = f"Sinus {f} Hz"
        # TODO fix rate
        self.rate = config.SAMPLING_FREQUENCY

    def loadAudioFile(self):
        self.rate, self.tamp = audiofile.read(config.AUDIO_FILE_TEST)
        self.codec = "WAV"
        self.temporalAvailable = True
        self.npts = len(self.tamp) * self.rate
        self.getTemporalVectorFromAudioFile()

    def getTemporalVectorFromAudioFile(self):
        self.t = audiodsp.getTemporalVector(self.tamp, fs=self.rate)

    def fft(self, iscomplex=False):
        f, famp, fampDb = audiodsp.getFft(
            t=self.t, tamp=self.tamp, fs=self.rate, N=self.npts)
        # get rid of imaginary part 
        if not iscomplex:
            self.famp = abs(famp)
            self.fampDb = abs(fampDb)
        self.setSpectralContent(f=f, famp=famp, fampDb=fampDb)
    
    def plot(self, space="time", mode="short", show=False):
        if mode == "short":
            if space == "time":
                audioplot.shortPlot(self.t, self.tamp, space="time")
            elif space == "spectral":
                audioplot.shortPlot(self.f, self.fampDb, space="spectral")
        else:
            logging.error("Plot not possible")
        
        if show == True:
            audioplot.pshow()


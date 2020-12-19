import os
import sys
import copy
from pathlib import Path

from lib import audiodsp, audiofile, audioplot, audiogenerator
from lib import config, tool

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
        self.fampDb = None
        self.fphase = None
        self.slicer = None
        self.temporalAvailable = False
        self.spectralAvailable = False
        self.infos = {
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
    
    def loadSinus(self, f=440, a=0.7):
        self.rate = config.SAMPLING_FREQUENCY
        self.setTemporalContent(*audiogenerator.generateSine(f=f, A=a))

    def loadAudioFile(self, filePath: str=None):
        if filePath is not None:
            filepath = filePath
        else:
            filepath = config.AUDIO_FILE_TEST
        self.rate, self.tamp, self.infos = audiofile.read(filepath, makeMono=True)
        self.t = audiodsp.getTemporalVector(self.tamp, fs=self.rate)
    
    def fft(self, iscomplex: bool=False):
        self.setSpectralContent(*audiodsp.getFft(t=self.t, tAmplitude=self.tamp, fs=self.rate))
    
    def ifft(self):
        self.tamp = audiodsp.getiFft(audiodsp.mergeFftVector(amplitude=self.famp, phase=self.fphase))

    def addSlicer(self, addAmps: bool=False):
        if not addAmps: self.slicer = Slicer(newFreqs=self.f)
        elif addAmps: self.slicer = Slicer(newFreqs=self.f, newAmps=audiodsp.mergeFftVector(self.famp, self.fphase))

    def plot(self, space="time", mode="short", show: bool=False):
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

    def tplot(self):
        self.plot(space="time")
    
    def fplot(self):
        self.plot(space="spectral")
    
    def callBoardControl(self):
        vect = [self.t, self.f]
        data = [[self.tamp], [self.fampDb]]
        audioplot.boardControl(vect=vect, data=data, additionalData=self.infos, legendList=["temporal", "spectral", "spectral2"])


class Slicer():
    def __init__(self, size: int=config.BANDS_SLICER_SIZE, newFreqs: list=None, newAmps: list=None):
        self.size = 10  #TODO to update
        self.bands = {}
        self.freqs = None
        self.amps = None
        self.ampsDb = None
        if newFreqs is not None: self.importNewFreqsArray(newFreqs)
        if newAmps is not None:self.importNewAmpsArray(newAmps)
        self.updateSlicer()
    
    def importNewAmpsArray(self, newAmps: list):
        self.amps = copy.deepcopy(newAmps)
        _amp, _phase = audiodsp.splitFftVector(newAmps)
        _ampDb = audiodsp.convertAmpToAmpDb(_amp)
        self.ampsDb = copy.deepcopy(audiodsp.mergeFftVector(_ampDb, _phase))
        del _amp, _ampDb, _phase

    def importNewFreqsArray(self, newFreqs: list):
        self.freqs = copy.deepcopy(newFreqs)
        self.freqsLenght = len(self.freqs)     

    def getfAmpBandBoudaries(self, bandId: int) -> (int, int):
        return self.bands[f'{bandId}']["_freqIdx"][0], \
               self.bands[f'{bandId + 1}']["_freqIdx"][0] - 1

    def updateSlicer(self):
        _freqs = copy.deepcopy(self.freqs)
        _amps = copy.deepcopy(self.amps)
        _ampsDb = copy.deepcopy(self.ampsDb)
        _bands = {}
        refFreqList = tool.getBandFrequencies(self.size)
        for idx in range(len(refFreqList)):
            _freqIdx = tool.getClosestIndexToTargetInArray(_freqs, refFreqList[idx])
            if len(_freqIdx) == 1:
                boundMin = _freqIdx[0]
            if idx + 1 < len(refFreqList):
                boundMax = tool.getClosestIndexToTargetInArray(_freqs, refFreqList[idx + 1])[0] - 1
            else:
                boundMax = len(_freqs) 
            _bands[f"{idx}"] = {
                "_id": idx,
                "_freqIdx": _freqIdx,
                "_f0": refFreqList[idx],
                "_f": _freqs[boundMin:boundMax],
                "_amps": _amps[boundMin:boundMax],
                "_ampsDb": _ampsDb[boundMin:boundMax]
            }
        self.bands = copy.deepcopy(_bands)
        del _bands, _freqs, _amps, _ampsDb, refFreqList, boundMax, boundMin
    
    def getEnergyOfAllBands(self):
        # Parseval theorem
        pass

    def plotSpectrumByAreas(self, ids: list=None):
        areas = []
        freqAxis = self.freqs
        if ids is None:
            for i, v in self.bands.items():
                areas.append(self.bands[f"{i}"]["_id"])
        else:
            areas = copy.deepcopy(ids)
        for index, v in enumerate(areas):
            audioplot.shortPlot(
                self.bands[f"{index}"]["_f"], self.bands[f"{index}"]["_ampsDb"],
                space='spectral')
        del areas
import copy

from lib import audiodata
from lib import audiodsp, audiofile, audioplot, audiogenerator
from lib import config, tool

class Slicer():
    def __init__(self, size: int=config.BANDS_SLICER_SIZE, newFreq: list=None, newAmp: list=None, newPhase: list=None):
        # newPhase is none means newAmp is complex
        self.size = 10  #TODO to update
        self.bands = {}
        self.freqs = None
        self.amp = None
        self.ampDb = None
        self.phase = None
        if newFreq is not None: self.importNewFreqArray(newFreq)
        if newAmp is not None: self.importNewAmpArray(newAmp, newPhase)
        self.updateSlicer()
    
    def importNewAmpArray(self, newAmp: list, newPhase: list=None):
        # newPhase is none means newAmp is complex
        if newPhase is None:
            _amp, _phase = copy.deepcopy(audiodsp.splitFftVector(newAmp))
        else:
            _amp = copy.deepcopy(newAmp)
            _phase = copy.deepcopy(newPhase)
        _ampDb = tool.convertAmpToAmpDb(_amp)
        self.amp = copy.deepcopy(_amp)
        self.ampDb = copy.deepcopy(_ampDb)
        self.phase = copy.deepcopy(_phase)
        del _amp, _ampDb, _phase

    def importNewFreqArray(self, newFreq: list):
        self.freqs = copy.deepcopy(newFreq)
        self.freqsLenght = len(self.freqs)     

    def getfAmpBandBoudaries(self, bandId: int) -> (int, int):
        # wtf ?
        return self.bands[f'{bandId}']["_freqIdx"][0], \
               self.bands[f'{bandId + 1}']["_freqIdx"][0] - 1

    def updateSlicer(self):
        _freqs = copy.deepcopy(self.freqs)
        _amp = copy.deepcopy(self.amp)
        _ampDb = copy.deepcopy(self.ampDb)
        _phase = copy.deepcopy(self.phase)
        _bands = {}
        # get "slicing method" frequency list
        # can be updated with other slicing methods
        # this is where number of bands is defined
        refFreqList = tool.getBandFrequencies(self.size)
        # creates and fills n bands
        for idx in range(len(refFreqList)):
            _freqIdx = tool.getClosestIndexToTargetInArray(_freqs, refFreqList[idx])
            if len(_freqIdx) == 1:
                boundMin = _freqIdx[0]
            if idx + 1 < len(refFreqList):
                boundMax = tool.getClosestIndexToTargetInArray(_freqs, refFreqList[idx + 1])[0] + 1
            else:
                boundMax = len(_freqs) 
            _bands[f"{idx}"] = {
                "_id": idx,
                "_freqIdx": _freqIdx,
                "_f0": refFreqList[idx],
                "_f": _freqs[boundMin:boundMax],
                "_amp": _amp[boundMin:boundMax],
                "_ampDb": _ampDb[boundMin:boundMax],
                "_phase": _phase[boundMin:boundMax],
                "_energy": audiodsp.getBandEnergy(_amp[boundMin:boundMax], _phase[boundMin:boundMax])
            }
        self.bands = copy.deepcopy(_bands)
        del _bands, _freqs, _amp, _ampDb, _phase, refFreqList, idx, boundMax, boundMin
    
    def computeEnergyOfAreas(self, ids: list=None) -> list:
        # list allows to precise which bands to be computed
        # if ids is None ==> compute all bands
        energy = []
        if ids is None:
            areas = self.getAllBandsIdAvailable()
        else:
            areas = copy.deepcopy(ids)
        for index in areas:
            energy.append(audiodsp.getBandEnergy(self.bands[f"{index}"]["_amp"], self.bands[f"{index}"]["_phase"]))
        return energy 
        del energy, areas, index

    def plotSpectrumByAreas(self, ids: list=None):
        if ids is None:
            areas = self.getAllBandsIdAvailable()
        else:
            areas = copy.deepcopy(ids)
        for index, v in enumerate(areas):
            audioplot.shortPlot(
                self.bands[f"{v}"]["_f"], self.bands[f"{v}"]["_ampDb"],
                space='spectral')
        del areas, index, v
    
    def getAllBandsIdAvailable(self) -> list:
        areas = []
        for i, v in self.bands.items():
            areas.append(self.bands[f"{i}"]["_id"])
        return areas
        del areas, i, v
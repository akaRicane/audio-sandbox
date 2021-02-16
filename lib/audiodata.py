from lib import slicer
from lib import audiodsp, audiofile, audioplot, audiogenerator
from lib import config
import logging


class AudioData():
    def __init__(self):
        self.npts = None
        self.rate = config.SAMPLING_FREQUENCY
        self.t = None
        self.tamp = None
        self.f = None
        self.w = None
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

    def setSpectralContent(self, w: list, freq: list, amplitude: list,
                           amplitude_db: list = None, phase: list = None):
        self.w = w
        self.f = freq
        self.famp = amplitude
        self.fampDb = amplitude_db
        self.fphase = phase
        self.spectralAvailable = True

    def loadSinus(self, f=440, a=0.7):
        self.rate = config.SAMPLING_FREQUENCY
        self.setTemporalContent(*audiogenerator.generateSine(f=f, a=a))

    def loadAudioFile(self, filePath: str = None):
        if filePath is None:
            filePath = config.AUDIO_FILE_TEST
        self.rate, self.tamp, self.infos = audiofile.read(
            filePath, makeMono=True)
        self.t = audiodsp.getTemporalVector(self.tamp, fs=self.rate)

    def fft(self, iscomplex: bool = False):
        self.setSpectralContent(
            *audiodsp.getFft(t=self.t, tAmplitude=self.tamp, fs=self.rate))

    def ifft(self):
        self.tamp = audiodsp.getiFft(audiodsp.mergeFftVector(
            amplitude=self.famp, phase=self.fphase))

    def addSlicer(self, addAmp: bool = True):
        if not addAmp:
            self.slicer = slicer.Slicer(newFreq=self.f)
        else:
            self.slicer = slicer.Slicer(
                newFreq=self.f, newAmp=audiodsp.mergeFftVector(self.famp,
                                                               self.fphase))

    def plot(self, space="time", mode="short",
             normFreqs: bool = False, show: bool = False):
        # FIXME Are legendlist useful here ?
        legendList = []
        if mode == "short":
            if space == "time":
                audioplot.shortPlot(self.t, self.tamp, space=space)
                legendList.append("Time Plot")
            elif space == "spectral":
                if normFreqs:
                    audioplot.shortPlot(self.w, self.fampDb, space=space,
                                        scale='semilog', isNormalizedAxis=True)
                    legendList.append("Spectral Plot, normalized frequencies")
                else:
                    audioplot.shortPlot(self.f, self.fampDb,
                                        space=space, scale='semilog',
                                        isNormalizedAxis=False)
                    legendList.append("Spectral Plot")
        else:
            logging.error("Plot not possible")
        if show:
            audioplot.pshow(legend=legendList)
        del legendList, mode

    def tplot(self, isNewFigure: bool = False):
        self.plot(space="time")

    def fplot(self, normFreqs: bool = False, isNewFigure: bool = False):
        self.plot(space="spectral", normFreqs=normFreqs)

    def callBoardControl(self):
        vect = [self.t, self.f]
        data = [[self.tamp], [self.fampDb]]
        audioplot.boardControl(vect=vect, data=data, additionalData=self.infos,
                               legendList=["temporal", "spectral", "spect2"])
        del vect, data

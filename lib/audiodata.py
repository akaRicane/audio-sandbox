import logging
import os
import sys
sys.path.append(os.getcwd())
from lib import slicer
from lib import audiodsp, audiofile, audioplot, audiogenerator
from lib import config, tool


class AudioData():
    def __init__(self, rate: int = config.SAMPLING_FREQUENCY):
        self.npts = None
        self.rate = rate
        self.fftsize = config.FFT_SIZE
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

    def rt_chunk_anaysis(self, chunk):
        self.tamp = chunk
        self.famp = audiodsp.chunk_fft(self.tamp, self.fftsize)

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

    def load_audio_array(self, audio_array: list):
        duration = len(audio_array) / self.rate
        time_vector = tool.create_time_basis(fs=self.rate, duration=duration)
        self.setTemporalContent(time_vector, audio_array)

    def loadSinus(self, f=440, gain=0.7):
        self.setTemporalContent(*audiogenerator.generateSine(f0=f, gain=gain, fs=self.rate))

    def load_audiofile_from_filepath(self, filepath: str = None):
        if filepath is None:
            filepath = config.AUDIO_FILE_TEST
        self.tamp, self.rate = audiofile.load_from_filepath(filepath)
        self.t = audiodsp.getTemporalVector(self.tamp, fs=self.rate)
        print(f"{filepath} has been loaded")

    def fft(self, iscomplex: bool = False):
        self.setSpectralContent(
            *audiodsp.getFft(tAmplitude=self.tamp,
                             N=self.fftsize, fs=self.rate))

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

    def compute_audio_array_analysis(self, audio_array: list):
        self.load_audio_array(audio_array)
        self.fft(iscomplex=False)
        self.build_signal_visualizer()

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
                                        scale='lin', isNormalizedAxis=True)
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

    def tplot(self, isNewFigure: bool = False):
        self.plot(space="time", show=True)

    def fplot(self, normFreqs: bool = False, isNewFigure: bool = False):
        self.plot(space="spectral", normFreqs=normFreqs, show=True)

    def build_signal_visualizer(self):
        self.signal_visualizer = audioplot.SignalVisualizer(self.t, self.tamp,
                                                            self.f, self.fampDb)

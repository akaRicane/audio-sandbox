import numpy as np
import logging
import scipy.signal as signal
from scipy.signal import butter, sosfilt, sosfreqz
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.getcwd())
from lib import audioplot, config


class AudioFilter():
    # designed to be one item with one filter
    # usage would be:
    # myFilter = audiofiltering.AudioFilter()
    # myFilter.getBandPassSosCoefs(lowcut, highcut, order=6)
    # my_y = myFilter.returnFilteredData(x)

    def __init__(self, fs: int = config.SAMPLING_FREQUENCY):
        self.coefs = None
        self.type = "empty"
        self.order = None
        self.fs = fs
        self.freqs = None
        self.fresponse = None

    def getBandPassSosCoefs(self, lowcut, highcut, order=config.BANDPASS_DEFAULT_ORDER):
        nyq = 0.5 * self.fs
        low = lowcut / nyq
        high = highcut / nyq
        self.coefs = butter(order, [low, high], btype='band', output='sos')
        self.type = "sos"
        self.order = order
        del nyq, low, high

    def getHighPassFiltSosCoefs(self, order: int = 4, fcut: float = 1000):
        # wn = 2 * np.pi * fcut / 20000
        self.coefs = signal.butter(order, fcut, btype="high", output="sos", analog="True")
        self.type = "sos"

    def filtBroadcast(self, dataToFilter: list) -> list:
        pass

    def returnFilteredData(self, data: list):
        if self.type == "sos":
            return sosfilt(self.coefs, data)
        # add elif for other methods
        else:
            logging.error("Asked filtering data with unexpected filter type coefs")

    def computeFilterFreqResp(self):
        if self.type == "sos":
            self.freqs, self.fresponse = signal.sosfreqz(sos=self.coefs, worN=2000)
        else:
            logging.error("Asked computing filter frequency response with unexpected filter type coefs")

    def impulseRespOfFilter(self):
        t = np.arange(1024.0) / self.fs
        impulse = signal.unit_impulse(1024)
        response = self.returnFilteredData(impulse)
        audioplot.shortPlot(vect=t, data=impulse)
        audioplot.shortPlot(vect=t, data=response)
        audioplot.pshow(legend=["impulse", "response"])

    def plotFilterResponse(self):
        audioplot.shortPlot(vect=(self.fs * 0.5 / np.pi) * self.freqs, data=abs(self.fresponse))
       

    # def equalizer_10band (data, fs, gain1=0, gain2=0, gain3=0, gain4=0, gain5=0, gain6=0, gain7=0, gain8=0, gain9=0, gain10=0):
    #     band1 = bandpass_filter(data, 20, 39, fs, order=2)* 10**(gain1/20)
    #     band2 = bandpass_filter(data, 40, 79, fs, order=3)*10**(gain2/20)
    #     band3 = bandpass_filter(data, 80, 159, fs, order=3)*10**(gain3/20)
    #     band4 = bandpass_filter(data, 160, 299, fs, order=3)* 10**(gain4/20)
    #     band5 = bandpass_filter(data, 300, 599, fs, order=3)* 10**(gain5/20)
    #     band6 = bandpass_filter(data, 600, 1199, fs, order=3)* 10**(gain6/20)
    #     band7 = bandpass_filter(data, 1200, 2399, fs, order=3)* 10**(gain7/20)
    #     band8 = bandpass_filter(data, 2400, 4999, fs, order=3)* 10**(gain8/20)
    #     band9 = bandpass_filter(data, 5000, 9999, fs, order=3)* 10**(gain9/20)
    #     band10 = bandpass_filter(data, 10000, 20000, fs, order=3)* 10**(gain10/20)
    #     signal = band1 + band2 + band3 + band4 + band5 + band6 + band7 + band8 + band9 + band10
    #     return signal
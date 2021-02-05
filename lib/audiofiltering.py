import numpy as np
import scipy as sp
import scipy.signal as signal
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.getcwd())
from lib import audioplot

class AudioFilter():
    # designed to be one item with one filter
    # usage would be y_filtered = audiofiltering.applyFilter(y, **args)
    def __init__(self):
        self.coefs = (None, None)
        self.type = "empty"

    def getHighPassFiltSosCoefs(self, order: int=4, fcut: float=1000):
        # wn = 2 * np.pi * fcut / 20000
        self.coefs = signal.butter(order, fcut, btype="high", output="sos", analog="True")
        self.type = "sos"

    def filtBroadcast(self, dataToFilter: list) -> list:
        # get HP and LP sos coefs
        # filter data 
        pass

    def addBandPassFilt(self):
        ...

    def impulseRespOfFilter(self):
        impulse = signal.unit_impulse(512)
        if self.type == "sos":
            response = signal.sosfilt(sos=self.coefs, x=impulse) 
            w, h = signal.sosfreqz(sos=self.coefs, worN=512)
            sos = signal.butter(4, 1000, 'high', output="sos", analog=True)
            w, h = signal.sosfreqz(sos)
        else:
            response = signal.lfilter(b=self.coefs[0], a=self.coefs[1], x=impulse)
            w, h = signal.freqs(b=self.coefs[0], a=self.coefs[1])
        
        plt.semilogx(w, 20 * np.log10(abs(h)))

        plt.title('Butterworth filter frequency response')
        plt.xlabel('Frequency [radians / second]')
        plt.ylabel('Amplitude [dB]')

        plt.grid(True)
        plt.margins(0, 0.1)
        plt.grid(which='both', axis='both')
        plt.axvline(1000, color='green') # cutoff frequency
        plt.show()
    
    # def bandpass_filter(data, lowcut, highcut, fs, order=5):
    #     nyq = 0.5 * fs
    #     low = lowcut / nyq
    #     high = highcut / nyq
    #     b, a = butter(order, [low, high], btype='bandpass')
    #     filtered = lfilter(b, a, data)
    #     return filtered

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
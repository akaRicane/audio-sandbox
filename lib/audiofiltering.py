import numpy as np
import scipy as sp
import scipy.signal as signal
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.getcwd())
from lib import audioplot

class AudioFilter():
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

    def impulseRespOfFilter(self):
        impulse = signal.unit_impulse(512)
        if self.type == "sos":
            response = signal.sosfilt(sos=self.coefs, x=impulse) 
            w, h = signal.sosfreqz(sos=self.coefs)
        else:
            response = signal.lfilter(b=self.coefs[0], a=self.coefs[1], x=impulse)
            w, h = signal.freqs(b=self.coefs[0], a=self.coefs[1])
        
        plt.semilogx(w, 20 * np.log10(abs(response)))
        plt.title('Butterworth filter frequency response')
        plt.xlabel('Frequency [radians / second]')
        plt.ylabel('Amplitude [dB]')
        # plt.margins(0, 0.1)
        plt.grid(which='both', axis='both')
        plt.axvline(1000, color='green') # cutoff frequency
        plt.show()
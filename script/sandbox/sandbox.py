import sys
import os

import matplotlib.pyplot as plt

sys.path.append(os.getcwd())
from lib import audio, audioplot

def main():
    # class items
    signal = audio.AudioItem()
    signal.addSinusAsNewChannel()

    signal.data[0].tplot()
    # plt.plot(signal.data[0].tamp, 'g')
    signal.data[0].fft()
    # signal.data[0].fplot()
    # audioplot.pshow()
    signal.cloneChannel(0)
    signal.data[1].ifft()
    signal.data[1].tplot()
    # plt.plot(signal.data[1].tamp, 'b')
    signal.data[1].fft()
    # signal.data[1].fplot()
    audioplot.pshow(["original", "ifft"])
    # to fix: ifft <<<-----


if __name__ == "__main__":
    main()
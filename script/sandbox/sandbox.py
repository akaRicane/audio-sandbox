import sys
import os

sys.path.append(os.getcwd())
from lib import audio, audioplot

def main():
    # class items
    signal = audio.AudioItem()
    signal.addSinusAsNewChannel()
    
    signal.data[0].fft()
    signal.data[0].fplot()
    audioplot.pshow()


if __name__ == "__main__":
    main()
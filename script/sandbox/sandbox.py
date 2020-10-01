import sys
import os
from pathlib import Path
import matplotlib.pyplot as plt

sys.path.append(os.getcwd())
from lib import audio

def main():

    # class items
    joyca = audio.AudioItem()
    joyca.loadAudioFile()
    joyca.setToMono()
    joyca.fft()
    joyca.plot(show=True)
    joyca.plot(show=True, space="spectral")
    # filtrer la voix

if __name__ == "__main__":
    main()
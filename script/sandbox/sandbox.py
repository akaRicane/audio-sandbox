import sys
import os

sys.path.append(os.getcwd())
from lib import audio

def main():
    # class items
    joyca = audio.AudioItem()
    joyca.addSinusAsNewChannel()
    joyca.makeStereo()
    joyca.setAudioItemToMono()

    # sub-class methods
    joyca.data[0].fft()
    joyca.data[0].plot(show=True)
    joyca.data[0].plot(show=True, space="spectral")
    # filtrer la voix

if __name__ == "__main__":
    main()
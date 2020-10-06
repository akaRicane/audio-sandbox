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
    # joyca.data[0].fft(iscomplex=False)
    # joyca.plot(show=True)
    # joyca.plot(show=True, space="spectral")
    # filtrer la voix

if __name__ == "__main__":
    main()
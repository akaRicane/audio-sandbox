import sys
import os

sys.path.append(os.getcwd())
from lib import audio, audioplot

def main():
    # class items
    joyca = audio.AudioItem()
    joyca.addSinusAsNewChannel()
    joyca.makeStereo()
    joyca.setAudioItemToMono()

    # sub-class methods
    joyca.data[0].fft()
    joyca.data[0].ifft()
    
    joyca.data[0].fplot()
    joyca.data[0].tplot()
    # joyca.data[0].callBoardControl()
    # filtrer la voix
    audioplot.pshow()
if __name__ == "__main__":
    main()
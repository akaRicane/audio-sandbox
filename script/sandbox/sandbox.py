import os
import sys
sys.path.append(os.getcwd())
from lib import audioplot, audiodata  # noqa E402


if __name__ == "__main__":
    source = audiodata.AudioData()
    # source.loadAudioFile()
    source.loadSinus()
    source.fft()
    source.fplot(normFreqs=False)
    audioplot.pshow()
    source.fplot(normFreqs=True)
    audioplot.pshow()

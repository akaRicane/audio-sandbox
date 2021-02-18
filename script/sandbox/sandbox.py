import os
import sys
sys.path.append(os.getcwd())
from lib import audioplot, audiodata  # noqa E402


if __name__ == "__main__":
    legendList = []
    source = audiodata.AudioData()
    fsTests = [11000, 22050, 44100, 48000, 88200, 96000]
    # fsTests = [44100]
    # source.loadAudioFile()
    for fs in fsTests:
        source.rate = fs
        source.loadSinus()
        print(f"Size of signal: {len(source.t)} points")
        for i in [1, 2, 4]:
            source.fftsize = 512 * i
            source.fft()
            source.fplot(normFreqs=False)
            legendList.append(f"{source.rate} Hz / {source.fftsize} fft points")
            print(f"fft freq len: {len(source.f)} fft points")
    audioplot.pshow(legendList)

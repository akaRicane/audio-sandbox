import os
import sys
sys.path.append(os.getcwd())
from lib import audioplot, audiodata, audiodsp, tool, config  # noqa E402


if __name__ == "__main__":
    legendList = []
    source = audiodata.AudioData() # <-- stepped sine mesuré
    f_sin = 3175.3548  # Hz <-- on sait quelle freq du stpsine est jouée
    source.rate = 44100
    source.fftsize = int(f_sin)
    df = source.rate / source.fftsize
    fTests = [f_sin, 2 * f_sin + 0.35*(df / 2.0)]
    # source.loadAudioFile()
    for f_test in fTests:
        source.loadSinus(f=f_test)
        print(f"Size of signal: {len(source.t)} points")
        source.fft()
        source.fplot(normFreqs=False)
        legendList.append(f"{f_test} Hz")
        # energy in all signal
        energy_allsignal = 0
        for value in source.famp:
            energy_allsignal += value ** 2
        # need to zero the peak, fin idx
        idxPeak = tool.getClosestIndexToTargetInArray(source.famp, f_test)
        # put 0 around peak
        source.fampDb[idxPeak[0]] = 0
        for i in range(5):
            source.famp[idxPeak[0] - i] = 0
            source.famp[idxPeak[0] + i] = 0
        # energy in signal - peak
        energy_remaining = 0
        for value in source.famp:
            energy_remaining += value ** 2
        thdn = (energy_remaining / energy_allsignal)
        source.fplot()
        legendList.append(f"{f_test} Hz / THDN: {thdn}")
    print(f"fs: {source.rate} / {source.fftsize} fft points")
    audioplot.pshow(legendList)

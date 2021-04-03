import os
import sys
sys.path.append(os.getcwd())
from script.sandbox import ricanelib
from lib import audioplot_qt as qt_plot  # noqa E402
from lib import audiogenerator  # noqa E402
from modules import player as Player

if __name__ == "__main__":
    # sweep, tsweep = audiogenerator.generateSweptSine(amp=0.75*100,
    #                                                  f0=20,
    #                                                  f1=20000,
    #                                                  duration=1.0,
    #                                                  fs=44100,
    #                                                  fade=True,
    #                                                  novak=True)
    sweep2, tsweep2 = audiogenerator.generateSweptSine(amp=0.75,
                                                       f0=1500,
                                                       f1=5500,
                                                       duration=1.0,
                                                       fs=44100,
                                                       fade=True,
                                                       novak=True)
    # visualizer = qt_plot.LabVisualizer(2, sweep.tolist(), sweep2.tolist())
    # visualizer = qt_plot.LabVisualizer(10, session.Player.processed)

    session = AudioCore.AudioCore()
    session.Player.init_stream_with_audio_array(sweep2, 44100)
    session.Visualizer = qt_plot.SignalVisualizer(buffer_size=session.Player.buffer_size,
                                                  rate=session.Player.rate,
                                                  n_channels=session.Player.n_channels)

import os
import sys
import ricanelib
import matplotlib.pyplot as plt
import sounddevice as sd
import soundfile as sf

sys.path.append(os.getcwd())
from lib import audiogenerator, audiodsp  # noqa E402 
from lib import tool, config  # noqa E402
from modules import audiocore as AudioCore  # noqa E402
from modules import player as Player  # noqa E402

# Global Parameters
rate = config.SAMPLING_FREQUENCY
tsweep, sweep = audiogenerator.generateSweptSine(amp=0.5,
                                                 f0=150,
                                                 f1=10000,
                                                 duration=1.0,
                                                 fs=rate,
                                                 fade=True,
                                                 novak=True)
tsine, sine = audiogenerator.generateSine(f0=500, gain=0.8, fs=rate)


def main1():  # plot chunk by chunk after process
    # load audio as wave_read object
    khi_project = AudioCore.AudioCore()
    # load filtering modules
    # khi_project.ModulesRack.add_new_module(ricanelib.ModuleItem(type="Audio_filter_rt",
    #                                                             subtype="rt_bandpass"))

    """Use as static ~ load file or play signal"""
    # khi_project.Player.config_stream_with_filepath(config.AUDIO_FILE_SWEEP)
    khi_project.Player.config_stream_with_audio_array(sine, rate)
    khi_project.play_once_until_end()

    """Use as dynamic ~ read input stream and process it"""
    # khi_project.record_stream_input_during(duration=1.0, rate=rate)
    # khi_project.Player._close()

    """Visualization after running program """
    print("Plot is opening !")
    # khi_project.init_labvisualizer()
    chunck_size = khi_project.Player.buffer_size
    data = khi_project.Player.original
    for i in range(khi_project.Player.original_size-1):
        fig, (ax, ax2) = plt.subplots(2, 1)
        chunck = data[chunck_size * i: chunck_size * (i+1) - 1]
        w, f, data_fft, data_fft_db, phi = audiodsp.getFft(chunck, fs=khi_project.Player.rate)
        ax.plot(data)
        ax2.semilogx(f, data_fft_db)
        plt.show()

    print("\nBye bye")


if __name__ == "__main__":
    audiofile = config.AUDIO_FILE_JOYCA
    data, fs = sf.read(audiofile)
    sd.play(data, fs)
    sd.wait()

    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])
    if args.filename is None:
        args.filename = tempfile.mktemp(prefix='delme_rec_unlimited_',
                                        suffix='.wav', dir='')

    # Make sure the file is opened before recording anything:
    with sf.SoundFile(args.filename, mode='x', samplerate=args.samplerate,
                      channels=args.channels, subtype=args.subtype) as file:
        with sd.InputStream(samplerate=args.samplerate, device=args.device,
                            channels=args.channels, callback=callback):
            print('#' * 80)
            print('press Ctrl+C to stop the recording')
            print('#' * 80)
            while True:
                file.write(q.get())
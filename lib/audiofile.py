import logging
import numpy as np
import sounddevice as sd
import soundfile as sf
import wave


def load_from_filepath(filepath: str) -> (np.array, int):
    """[summary]

    Args:
        filepath (str): [audiofile filepath]

    Returns:
        audio_signal (np.array): [audio array * n_channels]
        samplerate (int): samplerate
    """

    with open(filepath, 'rb') as f:
        audio_signal, samplerate = sf.read(f)
    return audio_signal, samplerate

def write_in_audiofile


def makeArrayMono(data):
    mono = []
    for idx, sample in enumerate(data):
        mono.append(sample[0])
    return mono


def read(filePath, makeMono=False):
    """ Read audio file from filepath
    Args:
        filePath (WindowsPath): [description]
        makeMono: if True, return only data monodimensional
    Returns:
        [int]: rate
        [numpy.array]: data
    """
    if filePath.suffix == ".wav":
        rate, data = wave.open(filePath, 'rb')
    # TODO add other codecs
    elif filePath.suffix == ".mp3":
        song = AudioSegment.from_mp3(filePath)
    else:
        logging.error("Audio codec unsupported !")
    codec = 'WAV'
    infos = {
        "codec": codec,
        "length": len(data) / rate,
        "nChannels": 2
    }
    if makeMono:
        data = makeArrayMono(data)
        infos["nChannels"] = 1
    return rate, data, infos


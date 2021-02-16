import logging
from pydub import AudioSegment
from scipy.io import wavfile


def dispAudioFileInfos(rate: int, arrayLength: int, codec: str):
    # TODO to fix and complete
    audioLength = round(arrayLength / rate * 1000, 2)
    logging.warning(f"---- Audio file opened successfully ----\n"
                    f"Codec: {codec} | Rate: {rate} Hz| Length: {audioLength} ms")


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
        rate, data = wavfile.read(filePath)
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


def openWithFfmepg(filePath):
    cmd = f'ffmpeg -i {filePath}'

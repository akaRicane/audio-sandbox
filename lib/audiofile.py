import logging
from pathlib import Path
from pydub import AudioSegment
from scipy.io import wavfile


def dispAudioFileInfos(rate: int, arrayLength: int, codec: str):
    # TODO to fix and complete
    audioLength = round(arrayLength / rate * 1000, 2)
    logging.warning(f"---- Audio file opened successfully ----\n"
                    f"Codec: {codec} | Rate: {rate} Hz| Length: {audioLength} ms")


def read(filePath):
    """ Read audio file from filepath
    Args:
        filePath (WindowsPath): [description]
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
    return rate, data
import os
import numpy as np
import soundfile as sf
from pathlib import Path


def load_from_filepath(filepath: Path) -> (np.array, int):
    """Load audiofile from file with SoundDevice.
    Returns (frames * n_channels, rate)

    Args:
        filepath (str): [audiofile filepath]

    Returns:
        audio_signal (np.array): [frames * n_channels]
        rate (int): rate
    """

    with open(filepath, 'rb') as f:
        audio_signal, rate = sf.read(f)
    return audio_signal, rate


def write_in_audiofile(filepath: str, filename: str, format: str,
                       audio_signal: np.array, rate: int,
                       subtype: str = None,
                       overwrite: bool = True) -> bool:
    """Write an audio_signal (frame * n_channels) to an audiofile
    with a given format and compatible subtype. Overwrite existing
    file if specified.

    Args:
        filepath (str): [Repository location]
        filename (str): [Filename with its extension]
        format (str): [Extension written under format "WAV", "FLAC", etc]
        audio_signal (np.array): [audio signal to write]
        rate (int): [samplerate]
        subtype (str, optional): [Specific subtype]. Defaults to None.
        overwrite (bool, optional): [Overwrite existing file]. Defaults to True.

    Returns:
        bool: [True if success, False else]
    """
    full_path = Path(filepath, filename)
    success = False
    # check if given subtype is format-compatible
    if subtype is not None and\
       not sf.check_format(format=format, subtype=subtype):
        raise Exception(f"Given subtype ({subtype}) is not\
                        compatible with format ({format})")
    elif subtype is None:
        subtype = sf.default_subtype(format)
    # check if no similar file exist there or if permission and write
    if not check_if_file_exist(full_path) or overwrite is True:
        sf.write(full_path, audio_signal, rate, subtype)
        success = True
        print(f"{filename} has been created with {subtype} subtype")
    else:
        print("Cannot write audiofile")
    return success


def check_if_file_exist(filepath: str) -> bool:
    return os.path.isfile(filepath)

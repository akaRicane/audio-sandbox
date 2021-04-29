import os
import sys
import pytest
import numpy as np
from pathlib import Path
sys.path.append(os.getcwd())
from lib import audiofile, config  # noqa E402
######################
# We want to test audiofile.py
# -> load_from_filepath
#       check filepath is Path
#       check if unexisting file is catched
# -> write_in_audiofile
#


def test_load_from_filepath_fail():
    _str = "not a filepath"
    with pytest.raises(Exception):
        audiofile.load_from_filepath((_str))
    _int = 10
    with pytest.raises(Exception):
        audiofile.load_from_filepath((_int))
    _bool = False
    with pytest.raises(Exception):
        audiofile.load_from_filepath((_bool))


def test_load_from_filepath_not_found():
    # test done in ressources on audioFileTest.wav
    _str = "audioFileTest.wa"
    path = Path(config.AUDIO_RESSOURCES, _str)
    with pytest.raises(Exception):
        audiofile.load_from_filepath((path))


def test_load_from_filepath_success():
    # test done in ressources on audioFileTest.wav
    _str = "audioFileTest.wav"
    path = Path(config.AUDIO_RESSOURCES, _str)
    data, rate = audiofile.load_from_filepath(path)
    assert isinstance(data, np.ndarray)
    assert type(rate) is int

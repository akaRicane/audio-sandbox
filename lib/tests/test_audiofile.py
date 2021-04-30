import os
import sys
import pytest
import numpy as np
from pathlib import Path
sys.path.append(os.getcwd())
from lib import audiofile, config, tool  # noqa E402
######################
# We want to test audiofile.py
# -> load_from_filepath
#       check filepath is Path
#       check if unexisting file is catched
# -> write_in_audiofile
#       check if existing, write, check if still there
#       check if existing and overwrite to false
#       incompatible given subtype
#       create noisy signal
#           write it, load and check if signal is same
#           do it for multi sample rates


class TestLoad_from_filepath:

    def test_fail(self):
        _str = "not a filepath"
        with pytest.raises(Exception):
            audiofile.load_from_filepath((_str))
        _int = 10
        with pytest.raises(Exception):
            audiofile.load_from_filepath((_int))
        _bool = False
        with pytest.raises(Exception):
            audiofile.load_from_filepath((_bool))

    def test_not_found(self):
        # test done in ressources on audioFileTest.wav
        _str = "audioFileTest.wa"
        path = Path(config.AUDIO_RESSOURCES, _str)
        with pytest.raises(Exception):
            audiofile.load_from_filepath((path))

    def test_success(self):
        # test done in ressources on audioFileTest.wav
        _str = "audioFileTest.wav"
        path = Path(config.AUDIO_RESSOURCES, _str)
        data, rate = audiofile.load_from_filepath(path)
        assert isinstance(data, np.ndarray)
        assert type(rate) is int


class TestWrite_in_audiofile:

    _filename = "audioFileTest.wav"
    _path = config.AUDIO_RESSOURCES
    _format = 'WAV'
    _data = np.random.randn(10, 2)
    _rate = 44100

    def test_overwrite(self):
        assert tool.check_if_file_exist(Path(self._path, self._filename))\
            is True

    def test_no_overwrite(self):
        assert tool.check_if_file_exist(Path(self._path, self._filename))\
            is True
        assert audiofile.write_in_audiofile(self._path, self._filename,
                                            self._format, self._data,
                                            self._rate, overwrite=False)\
            is False

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
#       check if existing and overwrite to false
#       incompatible given subtype
#       create noisy signal
#           write it, load and check if signal is same
#           do it for multi sample rates


class TestAudiofile:
    # test done in ressources on audioFileTest.wav
    _filename = "audioFileTest.wav"
    _repo = config.AUDIO_BIN
    _path = Path(config.AUDIO_BIN, _filename)
    _format = 'WAV'
    _data = np.random.randn(1000, 2)
    _rate = config.DEFAULT_SAMPLERATE


class TestLoad_from_filepath(TestAudiofile):
    @pytest.mark.parametrize("call", ["not a filepath", 10, False])
    def test_fail_call(self, call):
        with pytest.raises(Exception):
            audiofile.load_from_filepath(call)

    def test_file_not_found(self):
        _str = "audioFileTest.wa"
        with pytest.raises(Exception):
            audiofile.load_from_filepath(Path(config.AUDIO_BIN, _str))

    def test_load_success(self):
        data, rate = audiofile.load_from_filepath(self._path)
        assert isinstance(data, np.ndarray)
        assert type(rate) is int


class TestWrite_in_audiofile(TestAudiofile):
    @pytest.mark.parametrize("_rate", [44100, 48000, 88200, 96000])
    @pytest.mark.parametrize("_format", ['WAV', 'FLAC'])
    def test_overwrite(self, _rate, _format):
        assert tool.check_if_file_exist(Path(self._repo, self._filename))\
            is True
        assert audiofile.write_in_audiofile(self._repo, self._filename,
                                            _format, self._data,
                                            _rate, overwrite=True)\
            is True

    def test_no_overwrite(self):
        assert tool.check_if_file_exist(Path(self._repo, self._filename))\
            is True
        assert audiofile.write_in_audiofile(self._repo, self._filename,
                                            self._format, self._data,
                                            self._rate, overwrite=False)\
            is False

    def test_wrong_subtype(self):
        _subtype = 'PCM_25'  # is an incorrect subtype
        with pytest.raises(Exception):
            audiofile.write_in_audiofile(self._repo, self._filename,
                                         self._format, self._data,
                                         self._rate, _subtype)


class TestAudiofile_reliability(TestAudiofile):
    @pytest.mark.parametrize("prate", [44100, 48000, 88200, 96000])
    @pytest.mark.parametrize("pformat", ['WAV', 'FLAC'])
    def test_write_reliability(self, prate, pformat):
        audiofile.write_in_audiofile(self._repo, self._filename,
                                     pformat, self._data,
                                     prate, overwrite=True)
        loaded_data, loaded_rate = audiofile.load_from_filepath(self._path)
        assert len(loaded_data) == len(self._data)
        assert loaded_rate == prate
        comparison = loaded_data == self._data
        assert comparison.all() == True  # should be True !

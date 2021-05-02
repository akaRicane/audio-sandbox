import os
import sys
import pytest
import numpy as np
sys.path.append(os.getcwd())
from lib import config, tool  # noqa E402
from lib import audiogenerator  # noqa E402
from lib.audiogenerator import AudioSignal # noqa E402

######################
# We want to test audiogenerator.py
# signal is a mono array (vect, mag)
#


class TestAudioSignal:
    _max_size = 1024
    _rate = config.DEFAULT_SAMPLERATE
    _data = np.random.randn(1000, 1)
    _test_signal = AudioSignal()


class TestGenerate_vect(TestAudioSignal):

    def test_format_error(self):
        _call = "unsupported"
        with pytest.raises(ValueError):
            self._test_signal.generate_vect(self._data, _call)

    def test_duration_without_rate(self):
        _wrong_rate = 40000
        assert _wrong_rate not in config.VALID_SAMPLERATES
        with pytest.raises(ValueError):
            self._test_signal.generate_vect(self._data,
                                            'duration',
                                            _wrong_rate)


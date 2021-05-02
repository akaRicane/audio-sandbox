import os
import sys
import pytest
import numpy as np
sys.path.append(os.getcwd())
from lib import config, tool  # noqa E402
from lib import audiogenerator  # noqa E402
from lib.audiogenerator import AudioSignal # noqa E402
from lib import errors  # noqa E402

######################
# We want to test audiogenerator.py
# signal is a mono array (vect, mag)
#


class TestAudioSignal:
    _max_size = 1024
    _rate = config.DEFAULT_SAMPLERATE
    _duration = config.DEFAULT_DURATION
    _data = np.random.randn(_max_size, 1)
    _test_signal = AudioSignal()


class TestGenerate_vect(TestAudioSignal):
    _call = "unsupported"
    _wrong_rate = 40000

    def test_success_via_init(self):
        _test_init = AudioSignal(self._max_size, 'max_size', self._rate)
        assert _test_init.rate == self._rate

    def test_format_error(self):
        with pytest.raises(errors.InvalidFormat):
            self._test_signal.generate_vect(self._data, self._call)

    def test_rate_error(self):
        with pytest.raises(errors.InvalidRate):
            self._test_signal.generate_vect(
                self._data, 'duration', self._wrong_rate)

    def test_duration_without_rate(self):
        with pytest.raises(ValueError):
            self._test_signal.generate_vect(self._data, 'duration')

    def test_max_size_succes(self):
        assert self._test_signal.generate_vect(
            self._max_size, 'max_size') is True
        assert np.size(self._test_signal.vect) == len(self._data)

    def test_duration_succes(self):
        assert self._test_signal.generate_vect(
            self._duration, 'duration', self._rate) is True
        assert np.size(self._test_signal.vect) \
            == self._rate * self._duration

    def test_consistency_in_formats(self):
        # both methods give same len if used samewise
        equivalent_len = self._duration * self._rate
        method1 = AudioSignal()
        method1.generate_vect(equivalent_len, 'max_size')
        method2 = AudioSignal()
        method2.generate_vect(self._duration, 'duration', self._rate)
        assert np.size(method1.vect) == np.size(method2.vect)


class TestSine(TestAudioSignal):

    _test_sine = AudioSignal()
    _f0 = np.random.rand(1) * 1000
    _gain = np.random.rand(1)

    def test_missing_vect(self):
        with pytest.raises(errors.MissingVect):
            self._test_sine.sine(self._f0, self._gain)

    def test_success(self):
        self._test_sine.generate_vect(self._max_size, 'max_size')
        self._test_sine.sine(self._f0, self._gain)

import os
import sys
import pytest
import numpy as np
sys.path.append(os.getcwd())
from lib import config, tool  # noqa E402
from lib import audiogenerator  # noqa E402
from lib.audiogenerator import AudioSignal  # noqa E402
from lib.audiogenerator import Sine, MultiSine  # noqa E402
from lib import errors  # noqa E402

######################
# We want to test audiogenerator.py
# signal is a mono array (vect, mag)
#


class TestAudioSignal:
    _max_size = 1024
    _format = 'max_size'
    _rate = config.DEFAULT_SAMPLERATE
    _duration = config.DEFAULT_DURATION
    _data = np.random.randn(_max_size, 1)
    _test_signal = AudioSignal(_rate, _max_size, _format)
    _test_sine = Sine(_rate, 440, 1.0, _max_size, _format)


class TestAdd_signal(TestAudioSignal):

    def test_same_format_succes(self):
        self._test_signal.signal = self._data
        assert self._test_signal.add_signal(
            self._test_sine.vect, self._test_sine.signal) is True


class TestGenerate_vect(TestAudioSignal):

    def test_success_via_init(self):
        _test_init = AudioSignal(self._rate, self._max_size, self._format)
        assert _test_init.rate == self._rate

    def test_format_fail(self):
        with pytest.raises(errors.InvalidFormat):
            self._test_signal.generate_vect(self._data, "unsupported")

    def test_max_size_succes(self):
        assert self._test_signal.generate_vect(self._max_size) is True
        assert np.size(self._test_signal.vect) == len(self._data)

    def test_duration_succes(self):
        assert self._test_signal.generate_vect(
            self._duration, 'duration') is True
        assert np.size(self._test_signal.vect) \
            == self._rate * self._duration

    def test_consistency_in_formats(self):
        # both methods give same len if used samewise
        equivalent_len = self._duration * self._rate
        method1 = AudioSignal(self._rate, equivalent_len, self._format)
        method2 = AudioSignal(self._rate, self._duration, 'duration')
        assert np.size(method1.vect) == np.size(method2.vect)


class TestSine(TestAudioSignal):

    pass


class TestMultiSine(TestAudioSignal):

    _f_list = [440, 842, 310]
    _gain_list = [0.2, 0.8, 0.6]

    def test_fail_call(self):
        _missing_gain = self._gain_list[:-1]
        with pytest.raises(errors.InvalidFormat):
            MultiSine(self._rate, self._f_list, _missing_gain)

    def test_gainlist_is_none(self):
        _gain_list_ones = [1, 1, 1]
        _test_none = MultiSine(
            self._rate, self._f_list)
        _test_ones = MultiSine(
            self._rate, self._f_list, _gain_list_ones)
        comparison = _test_none.signal == _test_ones.signal
        assert comparison.all() == True

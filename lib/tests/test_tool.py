import os
import sys
import pytest
import numpy as np
sys.path.append(os.getcwd())
from lib import config, tool  # noqa E402


class TestSum_arrays:

    @pytest.mark.parametrize(
        "array1, array2, check",
        [
            pytest.param(
                [1, 1, 1], [10, 11, 12], [11, 12, 13]),
            pytest.param(
                [1, 1, 1, 1], [10, 11, 12], [11, 12, 13, 1]),
            pytest.param(
                [1, 1, 1], [10, 11, 12, 13], [11, 12, 13, 13])
        ])
    def test_sum(self, array1, array2, check):
        _sum = tool.sum_arrays(array1, array2)
        comparison = _sum == check
        assert comparison.all() == True


class TestTempFiles:
    # _repository = config.AUDIO_BIN
    _data_mono = np.random.uniform(-1, 1, size=1024)
    _data_stereo = [_data_mono, _data_mono]

    def test_create_close_success(self):
        fd, filepath = tool.save_array_in_temp(self._data_mono)
        print(filepath)
        assert isinstance(filepath, str)
        assert tool.check_if_file_exist(filepath)
        tool.close_tempfile(fd, filepath)
        assert tool.check_if_file_exist(filepath) is False

    def test_load_array_robustness(self):
        fd, filepath = tool.save_array_in_temp(self._data_mono)
        data_temp = tool.load_array_from_temp(filepath)
        comparison = data_temp == self._data_mono
        assert comparison.all() == True
        tool.close_tempfile(fd, filepath)
        assert tool.check_if_file_exist(filepath) is False

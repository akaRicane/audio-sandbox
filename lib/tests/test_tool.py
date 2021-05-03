import os
import sys
import pytest
import numpy as np
sys.path.append(os.getcwd())
from lib import config, tool  # noqa E402


class TestSum_arrays:
    _size = 50
    _smaller_size = _size - 10
    _array1 = np.random.randn(_size, 1)
    _array2 = np.random.randn(_size, 1)
    _array3 = np.random.randn(_smaller_size, 1)

    def manual_sum(self, arrayA, arrayB):
        _check_sum = []
        for i in range(self._size):
            _check_sum.append(self._array1[i] + self._array2[i])

    def test_success(self):
        _sum = tool.sum_arrays(self._array1, self._array2)
        _check_sum = self.manual_sum(self._array1, self._array2)
        comparison = _sum == _check_sum
        assert comparison.all() == True

    def test_pad_success(self):
        _sum = tool.sum_arrays(self._array1, self._array3, pad=True)
        _check_sum = self.manual_sum(self._array1, self._array3)
        comparison = _sum == _check_sum
        assert comparison.all() == True

    def test_pad_flipped_args(self):
        _sum = tool.sum_arrays(self._array1, self._array3, pad=True)
        _sum2 = tool.sum_arrays(self._array3, self._array1, pad=True)
        comparison = _sum == _sum2
        assert comparison.all() == True

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

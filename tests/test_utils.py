import numpy as np
import pytest
from utils import get_slice

@pytest.fixture
def sample_data():
    return np.arange(2*3*4).reshape(2, 3, 4)

@pytest.mark.parametrize("axis,index,expected_shape", [
    ('axial', 0, (2, 3)),
    ('coronal', 1, (2, 4)),
    ('sagittal', 1, (3, 4)),
])
def test_get_slice(sample_data, axis, index, expected_shape):
    result = get_slice(sample_data, axis, index)
    assert result.shape == expected_shape

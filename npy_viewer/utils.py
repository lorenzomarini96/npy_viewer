"""
Utility functions for image slicing operations.
"""

import numpy as np
from typing import Literal

AxisType = Literal['axial', 'coronal', 'sagittal']


def get_slice(data: np.ndarray, axis: AxisType, index: int) -> np.ndarray:
    """Return a slice along the given axis."""
    if data.ndim != 3:
        return data  # fallback for 2D images
    match axis:
        case 'axial':
            return data[:, :, index]
        case 'coronal':
            return data[:, index, :]
        case 'sagittal':
            return data[index, :, :]
    raise ValueError(f"Unknown axis: {axis}")

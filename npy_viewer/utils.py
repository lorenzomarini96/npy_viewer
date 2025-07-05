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
            return data[index, :, :] # Z-slice → [Y, X]
        case 'coronal':
            return data[:, index, :] # Y-slice → [Z, X]
        case 'sagittal':
            return data[:, :, index] # X-slice → [Z, Y]
    raise ValueError(f"Unknown axis: {axis}")

def apply_windowing(image: np.ndarray, center: float, width: float) -> np.ndarray:
    """
    Apply windowing to image (normalize to range [0, 1]).

    Args:
        image: input 2D numpy array
        center: window center
        width: window width

    Returns:
        Normalized image as float32
    """
    lower = center - width / 2
    upper = center + width / 2
    windowed = np.clip(image, lower, upper)
    return ((windowed - lower) / (upper - lower)).astype(np.float32)
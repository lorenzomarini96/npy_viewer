"""
This module defines the GUI for viewing .npy 2D/3D medical images in various anatomical views.
"""

import os
import logging
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from typing import Optional, Literal

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from npy_viewer.utils import get_slice

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ViewAxis = Literal['axial', 'coronal', 'sagittal']


class NpySliceViewer:
    """A simple GUI application to view slices of 2D/3D .npy images."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("NPY Slice Viewer")

        self.data: Optional[np.ndarray] = None
        self.axis: ViewAxis = 'axial'
        self.slice_index: int = 0

        self._setup_gui()

    def _setup_gui(self) -> None:
        """Configure GUI layout and widgets."""
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Load button
        ttk.Button(frame, text="Load .npy File", command=self._load_file).pack(pady=5)

        # Axis selector
        self.axis_combo = ttk.Combobox(frame, values=['axial', 'coronal', 'sagittal'], state='readonly')
        self.axis_combo.set('axial')
        self.axis_combo.pack()
        self.axis_combo.bind('<<ComboboxSelected>>', self._update_axis)

        # Slice index slider
        self.slider = tk.Scale(frame, from_=0, to=0, orient=tk.HORIZONTAL, command=self._update_slice)
        self.slider.pack(fill=tk.X)

        # Matplotlib figure
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _load_file(self) -> None:
        """Prompt user to load .npy file and initialize view."""
        file_path = filedialog.askopenfilename(filetypes=[("NumPy files", "*.npy")])
        if not file_path:
            return
        try:
            self.data = np.load(file_path)
            logger.info(f"Loaded file: {file_path}, shape={self.data.shape}")
            self._configure_slider()
            self._render_slice()
        except Exception as e:
            logger.error(f"Failed to load .npy file: {e}")
            messagebox.showerror("Error", f"Unable to load file:\n{e}")

    def _configure_slider(self) -> None:
        """Set up the slider range based on the selected axis and data shape."""
        if self.data is None:
            return
        axis_len = self._get_axis_length()
        self.slider.config(to=axis_len - 1)
        self.slider.set(0)
        self.slice_index = 0

    def _update_axis(self, event=None) -> None:
        """Handle axis view change."""
        self.axis = self.axis_combo.get()
        logger.info(f"Changed axis to: {self.axis}")
        self._configure_slider()
        self._render_slice()

    def _update_slice(self, index: str) -> None:
        """Update the displayed slice when the slider is moved."""
        self.slice_index = int(index)
        self._render_slice()

    def _get_axis_length(self) -> int:
        """Return number of slices along the selected axis."""
        assert self.data is not None
        match self.axis:
            case 'axial':
                return self.data.shape[2]
            case 'coronal':
                return self.data.shape[1]
            case 'sagittal':
                return self.data.shape[0]

    def _render_slice(self) -> None:
        """Render the selected image slice."""
        if self.data is None:
            return
        slice_img = get_slice(self.data, self.axis, self.slice_index)
        self.ax.clear()
        self.ax.imshow(slice_img, cmap='gray')
        self.ax.set_title(f"{self.axis.capitalize()} view - Slice {self.slice_index}")
        self.canvas.draw()

    def run(self) -> None:
        """Run the main GUI loop."""
        self.root.mainloop()

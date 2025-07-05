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

from npy_viewer.utils import get_slice, apply_windowing

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

        self.window_center: float = 0.0
        self.window_width: float = 1000.0
        self.colorbar = None
        self._pixel_info_text = None

        self._setup_gui()

    def _setup_gui(self) -> None:
        """Configure GUI layout and widgets."""
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Load button
        ttk.Button(frame, text="Load .npy File", command=self._load_file).pack(pady=5)

        # Anatomical view selector with full labels
        self.view_labels = {
            'Axial (Z slices – X/Y plane)': 'axial',
            'Coronal (Y slices – X/Z plane)': 'coronal',
            'Sagittal (X slices – Y/Z plane)': 'sagittal',
        }

        # Axis selector
        self.axis_combo = ttk.Combobox(frame, values=list(self.view_labels.keys()), state='readonly')
        self.axis_combo.set('Axial (Z slices – X/Y plane)')
        self.axis_combo.pack()
        self.axis_combo.bind('<<ComboboxSelected>>', self._update_axis)

        # Slice index slider
        self.slider = tk.Scale(frame, from_=0, to=0, orient=tk.HORIZONTAL, command=self._update_slice)
        self.slider.pack(fill=tk.X)

        # Matplotlib figure
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Bind mouse scroll events
        self.canvas.get_tk_widget().bind("<MouseWheel>", self._on_mouse_wheel)  # Windows/macOS
        self.canvas.get_tk_widget().bind("<Button-4>", self._on_mouse_wheel)    # Linux scroll up
        self.canvas.get_tk_widget().bind("<Button-5>", self._on_mouse_wheel)    # Linux scroll down
        
        self.canvas.mpl_connect("motion_notify_event", self._on_mouse_move)

    def _on_mouse_wheel(self, event) -> None:
        """Handle mouse wheel to change slice index."""
        if self.data is None:
            return

        max_index = self._get_axis_length() - 1

        # Windows/macOS
        if event.num == 0 or hasattr(event, "delta"):
            delta = int(event.delta / 120)
        # Linux
        elif event.num == 4:
            delta = 1
        elif event.num == 5:
            delta = -1
        else:
            delta = 0

        new_index = self.slice_index + delta
        new_index = max(0, min(max_index, new_index))

        if new_index != self.slice_index:
            self.slice_index = new_index
            self.slider.set(self.slice_index)  # Sync GUI slider
            self._render_slice()

    def _on_mouse_move(self, event) -> None:
        """Update pixel (x, y, value) overlay on mouse move."""
        if self.data is None or not event.inaxes:
            return

        x, y = int(event.xdata), int(event.ydata)
        slice_img = get_slice(self.data, self.axis, self.slice_index)

        if 0 <= y < slice_img.shape[0] and 0 <= x < slice_img.shape[1]:
            value = slice_img[y, x]
            info = f"x={x}, y={y}, value={value:.1f}"

            if self._pixel_info_text:
                self._pixel_info_text.set_text(info)

            self._pixel_info_text = self.ax.text(
                0.98, 0.02,
                info,
                transform=self.ax.transAxes,
                color='white',
                fontsize=9,
                verticalalignment='bottom',
                horizontalalignment='right',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='black', alpha=0.5)
            )
            self.canvas.draw()

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
        selected_label = self.axis_combo.get()
        self.axis = self.view_labels[selected_label]
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
                return self.data.shape[0] # Z
            case 'coronal':
                return self.data.shape[1] # Y
            case 'sagittal':
                return self.data.shape[2] # X
    
    def _render_slice(self) -> None:
        """Render the selected image slice."""
        if self.data is None:
            return
        slice_img = get_slice(self.data, self.axis, self.slice_index)
        vmin = slice_img.min()
        vmax = slice_img.max()

        self.ax.clear()
        self.ax.imshow(slice_img, cmap='gray')
        self.ax.set_title(f"{self.axis.capitalize()} view - Slice {self.slice_index}")
        self.canvas.draw()

        # Scrivi min/max in overlay sulla figura
        self.ax.text(
            0.02, 0.95,
            f"min: {vmin:.1f}   max: {vmax:.1f}",
            transform=self.ax.transAxes,
            color='white',
            fontsize=10,
            verticalalignment='top',
            horizontalalignment='left',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='black', alpha=0.5)
        )

        # Resetta overlay coordinate se presente
        if self._pixel_info_text:
            self._pixel_info_text.set_visible(False)
            self._pixel_info_text = None

        # Titolo con numero di slice
        total_slices = self._get_axis_length()
        self.ax.set_title(f"{self.axis.capitalize()} view – Slice {self.slice_index + 1} / {total_slices}")

        # Disegna tutto alla fine
        self.canvas.draw()


    def run(self) -> None:
        """Run the main GUI loop."""
        self.root.mainloop()

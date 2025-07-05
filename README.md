# NPY Viewer

A lightweight, interactive GUI tool to explore `.npy` 2D/3D medical image volumes in axial, sagittal, and coronal planes using Python and Matplotlib.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)

### Example Views

**Axial view**

![Axial](images/slice_view_axial.png)

**Coronal view**

![Coronal](images/slice_view_coronal.png)

**Sagittal view**

![Sagittal](images/slice_view_sagittal.png)

## Installation
### 1. Clone the repository

```bash
git clone https://github.com/lorenzomarini96/npy_viewer.git
cd npy_viewer
```
### 2. Create a virtual environment (recommended)
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```
### 3. Install dependencies and the package
```bash
pip install -r requirements.txt
pip install -e .
```
Or directly from GitHub:
```bash
pip install git+https://github.com/lorenzomarini96/npy_viewer.git
```
### Test your installation
After installation, verify that the package is working correctly:
```bash
# Optional: remove previous versions
pip uninstall npy_viewer

# Install in editable mode
pip install -e .

# To launch the GUI:
python gui.py
```
This will launch the GUI if everything is properly configured.

# Usage
After installing the package locally in editable mode, to launch the GUI viewer:

```bash
python gui.py
```

## Features

- Load .npy 2D or 3D image volumes
- Scroll through slices with slider
- Switch between axial / coronal / sagittal views
- Real-time display of pixel (x, y) and intensity value
- Overlay of slice min/max values

## Project Structure

```bash
(tf_metal) ➜  npy_viewer_project git:(main) ✗ tree
.
├── README.md
├── gui.py
├── npy_viewer
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-310.pyc
│   │   ├── main.cpython-310.pyc
│   │   ├── utils.cpython-310.pyc
│   │   └── viewer.cpython-310.pyc
│   ├── main.py
│   ├── utils.py
│   └── viewer.py
├── pyproject.toml
├── requirements.txt
├── setup.py
└── tests
    └── test_utils.py
```

# License
This project is licensed under the [GNU General Public License v3](https://www.gnu.org/licenses/gpl-3.0.en.html).  
You are free to use, modify, and redistribute it under the same license terms.
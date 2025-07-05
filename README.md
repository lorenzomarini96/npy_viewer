# NPY Viewer

A lightweight, interactive GUI tool to explore `.npy` 2D/3D medical image volumes in axial, sagittal, and coronal planes using Python and Matplotlib.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)

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

# Run the viewer
npy_viewer
```
This will launch the GUI if everything is properly configured.


# Usage
## Run the viewer
```bash
python -m npy_viewer.main
```
Or from anywhere (if installed globally):
```bash
npy_viewer_main
```



## Features

- Load .npy 2D or 3D image volumes
- Scroll through slices with slider
- Switch between axial / coronal / sagittal views
- Real-time display of pixel (x, y) and intensity value
- Overlay of slice min/max values

## Project Structure

```bash
npy_viewer/
├── __init__.py
├── main.py
├── viewer.py
├── utils.py
tests/
    └── test_utils.py
```

# License
This project is licensed under the [GNU General Public License v3](https://www.gnu.org/licenses/gpl-3.0.en.html).  
You are free to use, modify, and redistribute it under the same license terms.
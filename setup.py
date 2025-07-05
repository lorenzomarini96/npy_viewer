from setuptools import setup, find_packages

setup(
    name="npy_viewer",
    version="0.1.0",
    description="A simple GUI for viewing .npy images along axial, sagittal, and coronal views",
    author="Lorenzo Marini",
    author_email="lorenzo.marini.1996@gmail.com",
    packages=find_packages(),
    install_requires=[
        "numpy==1.26.4",
        "matplotlib==3.10.0",
    ],
    entry_points={
        "console_scripts": [
            "npy-viewer=npy_viewer.main:main",
        ],
    },
    python_requires=">=3.10",
)

from setuptools import setup, find_packages

setup(
    name="npy_viewer",
    version="0.1.0",
    description="A simple GUI for viewing .npy images along axial, sagittal, and coronal views",
    author="Lorenzo Marini",
    author_email="lorenzo.marini.1996@gmail.com",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.22",
        "matplotlib>=3.5",
    ],
    entry_points={
        "console_scripts": [
            "npy_viewer=npy_viewer.main:main",
        ],
    },
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)

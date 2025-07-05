"""Entry point for npy_viewer command-line script."""

from .viewer import NpySliceViewer
import logging

def main() -> None:
    """Entry point to launch the GUI application."""
    logging.basicConfig(level=logging.INFO)
    logging.info("Launching NPY Viewer GUI...")
    viewer = NpySliceViewer()
    viewer.run()

if __name__ == '__main__':
    main()




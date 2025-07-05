from .viewer import NpySliceViewer

def main() -> None:
    """Entry point to launch the GUI application."""
    viewer = NpySliceViewer()
    viewer.run()

if __name__ == '__main__':
    main()




# nuitka-project-if: {OS} in ("Windows")


from PySide6.QtWidgets import QApplication
from gui import MainWindow
from sys import (argv, exit)


if __name__ == "__main__":
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    exit(app.exec())
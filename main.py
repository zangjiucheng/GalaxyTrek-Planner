import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from src.ui import MyApp


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('data/icon.ico'))
    window = MyApp()
    window.show()
    # func = Func(window)
    sys.exit(app.exec())

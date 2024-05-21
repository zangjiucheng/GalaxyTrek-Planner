import sys

from PySide6.QtWidgets import QApplication

from src.ui import MyApp


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    # func = Func(window)
    sys.exit(app.exec())

import sys, os
from pathlib import Path
from PySide6.QtWidgets import  QApplication
from rova.ui.main_window import MainWindow
from rova.core.settings import AppSettings

def main():
    os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "1")

    app = QApplication(sys.argv)
    app.setApplicationName("RovaChatBot")

    settings = AppSettings.load()
    win = MainWindow(settings=settings)
    win.show()

    rc = app.exec()
    settings.save() # Persist them choice
    sys.exit(rc)

if __name__ == "__main__":
    main()
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from .sidebar import Sidebar
from .chat_page import ChatPage
from .theme import load_theme
from ..core.settings import AppSettings

class MainWindow(QMainWindow):
    def __init__(self, settings: AppSettings):
        super().__init__()
        self.setWindowTitle("Rova")
        self.settings = settings

        central = QWidget(); self.setCentralWidget(central)
        root = QHBoxLayout(central); root.setContentsMargins(12,12,12,12); root.setSpacing(12)

        self.sidebar = Sidebar()
        self.chat = ChatPage(settings=self.settings, apply_theme_cb=self.apply_theme)

        root.addWidget(self.sidebar); root.addWidget(self.chat, 1)

        self.apply_theme(self.settings.theme)

    def apply_theme(self, theme: str):
        self.setStyleSheet(load_theme(theme))

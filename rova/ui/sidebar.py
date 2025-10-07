from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton, QWidget, QSizePolicy
from PySide6.QtCore import Qt

class Sidebar(QFrame):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(14, 14, 14, 14)
        lay.setSpacing(12)

        avatar = QLabel("🙂")
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setFixedSize(48, 48)

        self.btn_chat = QPushButton("Chat")
        self.btn_home = QPushButton("Home")
        self.btn_settings = QPushButton("Settings")

        for b in (self.btn_chat, self.btn_home, self.btn_settings):
            b.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        lay.addWidget(avatar, alignment=Qt.AlignTop)
        lay.addSpacing(10)
        lay.addWidget(self.btn_chat)
        lay.addWidget(self.btn_home)
        lay.addStretch(1)
        lay.addWidget(self.btn_settings)

from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel
from PySide6.QtCore import Qt

class MessageBubble(QFrame):
    def __init__(self, text: str, role: str):
        super().__init__()
        cls = "UserBubble" if role == "user" else "AIBubble"
        self.setObjectName(cls)
        self.setProperty("class", cls)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(12, 8, 12, 8)
        lbl = QLabel(text)
        lbl.setWordWrap(True)
        lay.addWidget(lbl)
        if role == "user":
            lay.setAlignment(Qt.AlignRight)
        else:
            lay.setAlignment(Qt.AlignLeft)

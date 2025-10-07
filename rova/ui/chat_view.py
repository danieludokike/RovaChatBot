from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame, QSizePolicy
from PySide6.QtCore import Qt
from .message_bubble import MessageBubble

class ChatView(QWidget):
    def __init__(self):
        super().__init__()
        root = QVBoxLayout(self); root.setContentsMargins(0,0,0,0)
        self.scroll = QScrollArea(); self.scroll.setWidgetResizable(True)
        self.card = QFrame(); self.card.setObjectName("ChatCard")
        self.inner = QVBoxLayout(self.card); self.inner.setContentsMargins(16,16,16,16); self.inner.setSpacing(8)
        self.inner.addStretch(1)
        self.scroll.setWidget(self.card)
        root.addWidget(self.scroll)

    def add_message(self, text: str, role: str):
        bubble = MessageBubble(text, role)
        bubble.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.inner.insertWidget(self.inner.count()-1, bubble, alignment=Qt.AlignRight if role=="user" else Qt.AlignLeft)
        # autoscroll
        vs = self.scroll.verticalScrollBar()
        vs.setValue(vs.maximum())

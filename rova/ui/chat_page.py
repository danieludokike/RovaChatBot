from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QHBoxLayout, QLabel, QCheckBox
from PySide6.QtCore import Qt, QTimer

from .chat_view import ChatView
from .composer import Composer
from ..core.message import Message
from ..core.settings import AppSettings
from ..ui.theme import load_theme
from ..providers.mock_provider import MockProvider

class ChatPage(QWidget):
    def __init__(self, settings: AppSettings, apply_theme_cb):
        super().__init__()
        self.settings = settings
        self.apply_theme_cb = apply_theme_cb

        root = QVBoxLayout(self); root.setContentsMargins(12,12,12,12); root.setSpacing(12)

        # Header
        header = QFrame(); header.setObjectName("ChatHeader")
        h = QHBoxLayout(header); h.setContentsMargins(8,8,8,8)
        title = QLabel("Rova"); title.setObjectName("Title")
        dot = QLabel(); dot.setObjectName("StatusDot")
        theme_switch = QCheckBox("Dark")
        theme_switch.setChecked(self.settings.theme == "dark")
        theme_switch.stateChanged.connect(self.toggle_theme)

        h.addWidget(title); h.addWidget(dot, 0, Qt.AlignVCenter)
        h.addStretch(1); h.addWidget(theme_switch)
        root.addWidget(header)

        # Chat view
        self.view = ChatView()
        root.addWidget(self.view, 1)

        # Composer
        self.composer = Composer()
        self.composer.submitted.connect(self.on_submit)
        root.addWidget(self.composer)

        self.provider = MockProvider()

    def toggle_theme(self, _state: int):
        self.settings.theme = "dark" if self.settings.theme != "dark" else "light"
        self.apply_theme_cb(self.settings.theme)

    def on_submit(self, text: str):
        self.view.add_message(text, "user")
        # mock streaming
        msgs = [{"role":"user","content":text}]
        acc = ""
        def stream_tick(gen):
            nonlocal acc
            try:
                acc += next(gen)
                # live update last AI bubble (create on first tick)
                if not hasattr(self, "_ai_bubble"):
                    self.view.add_message("", "assistant")
                    self._ai_bubble = self.view.inner.itemAt(self.view.inner.count()-2).widget()
                self._ai_bubble.layout().itemAt(0).widget().setText(acc)
                QTimer.singleShot(10, lambda: stream_tick(gen))
            except StopIteration:
                self._ai_bubble = None
        stream_tick(iter(self.provider.stream(msgs)))

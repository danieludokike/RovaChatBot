from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QHBoxLayout, QLabel, QCheckBox
from PySide6.QtCore import Qt, QTimer
from .chat_view import ChatView
from .composer import Composer
from ..core.settings import AppSettings
from ..providers.factory import build_provider  # ✅ only import the factory

class ChatPage(QWidget):
    def __init__(self, settings: AppSettings, apply_theme_cb):
        super().__init__()
        self.settings = settings
        self.apply_theme_cb = apply_theme_cb

        # ✅ Load provider dynamically (OpenAI if set in .env)
        self.provider = build_provider(settings)
        print(f"✅ Using provider: {self.provider.name}")  # helpful log

        self._ai_label = None  # QLabel for live streaming text

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)

        # --- Header ---
        header = QFrame()
        header.setObjectName("ChatHeader")
        h = QHBoxLayout(header)
        h.setContentsMargins(8, 8, 8, 8)
        title = QLabel("Rova")
        title.setObjectName("Title")
        dot = QLabel()
        dot.setObjectName("StatusDot")
        theme_switch = QCheckBox("Dark")
        theme_switch.setChecked(self.settings.theme == "dark")
        theme_switch.stateChanged.connect(self._toggle_theme)
        h.addWidget(title)
        h.addWidget(dot)
        h.addStretch(1)
        h.addWidget(theme_switch)
        root.addWidget(header)

        # --- Chat View ---
        self.view = ChatView()
        root.addWidget(self.view, 1)

        # --- Composer ---
        self.composer = Composer()
        self.composer.submitted.connect(self._on_submit)
        root.addWidget(self.composer)

    def _toggle_theme(self, _):
        self.settings.theme = "dark" if self.settings.theme != "dark" else "light"
        self.apply_theme_cb(self.settings.theme)

    def _on_submit(self, text: str):
        """Send user input to AI provider and stream reply."""
        self.view.add_message(text, "user")

        msgs = [
            {"role": "system", "content": "You are Rova, a friendly helpful AI assistant."},
            {"role": "user", "content": text},
        ]

        gen = iter(self.provider.stream(msgs))
        acc = []

        def tick():
            nonlocal acc
            try:
                acc.append(next(gen))
                current = "".join(acc)
                if self._ai_label is None:
                    self._ai_label = self.view.add_message("", "assistant")
                self._ai_label.setText(current)
                QTimer.singleShot(8, tick)
            except StopIteration:
                self._ai_label = None
            except Exception as e:
                self.view.add_message(f"(Error: {e})", "assistant")
                self._ai_label = None

        QTimer.singleShot(0, tick)

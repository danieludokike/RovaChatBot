from PySide6.QtWidgets import QWidget, QHBoxLayout, QTextEdit, QPushButton
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QKeyEvent

class Composer(QWidget):
    submitted = Signal(str)

    def __init__(self):
        super().__init__()
        lay = QHBoxLayout(self); lay.setContentsMargins(12,12,12,12); lay.setSpacing(8)

        class _Edit(QTextEdit):
            submitted = Signal(str)
            def keyPressEvent(self, e: QKeyEvent):
                if e.key() in (Qt.Key_Return, Qt.Key_Enter):
                    if e.modifiers() & Qt.ShiftModifier:
                        # allow newline with Shift+Enter
                        return super().keyPressEvent(e)
                    # send on Enter
                    text = self.toPlainText().strip()
                    if text:
                        self.submitted.emit(text)
                        self.clear()
                    return
                super().keyPressEvent(e)

        self.edit = _Edit(); self.edit.setObjectName("Composer")
        self.edit.setPlaceholderText("Ask a question...")
        self.edit.setFixedHeight(44)
        self.edit.textChanged.connect(self._grow)
        self.edit.submitted.connect(lambda t: self.submitted.emit(t))

        self.btn = QPushButton("Send"); self.btn.setObjectName("SendBtn")
        self.btn.setEnabled(False); self.btn.clicked.connect(self._click_submit)

        lay.addWidget(self.edit); lay.addWidget(self.btn)

    def _grow(self):
        self.btn.setEnabled(bool(self.edit.toPlainText().strip()))
        h = self.edit.document().size().height() + 12
        self.edit.setFixedHeight(min(120, int(h)))

    def _click_submit(self):
        text = self.edit.toPlainText().strip()
        if text:
            self.submitted.emit(text)
            self.edit.clear()

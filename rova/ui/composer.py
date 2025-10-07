from PySide6.QtWidgets import QWidget, QHBoxLayout, QTextEdit, QPushButton
from PySide6.QtCore import Signal

class Composer(QWidget):
    submitted = Signal(str)

    def __init__(self):
        super().__init__()
        lay = QHBoxLayout(self); lay.setContentsMargins(12,12,12,12); lay.setSpacing(8)
        self.edit = QTextEdit(); self.edit.setObjectName("Composer")
        self.edit.setPlaceholderText("Ask a question...")
        self.edit.setFixedHeight(44)  # will grow
        self.edit.textChanged.connect(self._grow)
        self.btn = QPushButton("Send"); self.btn.setObjectName("SendBtn")
        self.btn.setEnabled(False)
        self.btn.clicked.connect(self._submit)
        lay.addWidget(self.edit); lay.addWidget(self.btn)

    def _grow(self):
        self.btn.setEnabled(bool(self.edit.toPlainText().strip()))
        doc_h = self.edit.document().size().height() + 12
        self.edit.setFixedHeight(min(120, int(doc_h)))

    def _submit(self):
        text = self.edit.toPlainText().strip()
        if text:
            self.submitted.emit(text)
            self.edit.clear()

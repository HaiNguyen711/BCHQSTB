import qtawesome as qta
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget


class Header(QWidget):
    def __init__(self, title, search_placeholder, search_callback, primary_button_text, primary_button_callback):
        super().__init__()
        self.search_callback = search_callback
        self.primary_button_callback = primary_button_callback
        self.setup_ui(title, search_placeholder, primary_button_text)

    def setup_ui(self, title, search_placeholder, primary_button_text):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self.title_label = QLabel(title)
        self.title_label.setObjectName('pageTitle')

        self.search = QLineEdit()
        self.search.setPlaceholderText(search_placeholder)
        self.search.setMinimumWidth(300)
        self.search.returnPressed.connect(self.search_callback)

        self.search_button = QPushButton(qta.icon('fa5s.search'), '')
        self.search_button.setObjectName('iconButton')
        self.search_button.clicked.connect(self.search_callback)

        self.primary_button = QPushButton(qta.icon('fa5s.plus'), '  ' + primary_button_text)
        self.primary_button.setObjectName('primaryButton')
        self.primary_button.clicked.connect(self.primary_button_callback)

        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(self.search)
        layout.addWidget(self.search_button)
        layout.addWidget(self.primary_button)

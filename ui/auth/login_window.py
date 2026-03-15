from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QWidget

from config.settings import APP_NAME, LOGIN_WINDOW_HEIGHT, LOGIN_WINDOW_WIDTH
from services.auth_service import login
from ui.auth.register_dialog import RegisterDialog
from ui.main_window import MainWindow


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_window = None
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(APP_NAME)
        self.setObjectName('loginWindow')
        self.setFixedSize(LOGIN_WINDOW_WIDTH, LOGIN_WINDOW_HEIGHT)

        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(36, 28, 36, 28)

        card = QWidget()
        card.setObjectName('loginCard')
        layout = QVBoxLayout(card)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(12)

        title = QLabel('Đăng nhập hệ thống BCHQS')
        title.setObjectName('loginTitle')
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel('Đăng nhập để quản lý công dân và nhập ngũ')
        subtitle.setObjectName('mutedLabel')
        subtitle.setAlignment(Qt.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Tên đăng nhập')

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Mật khẩu')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.returnPressed.connect(self.handle_login)

        login_btn = QPushButton('Đăng nhập')
        login_btn.setObjectName('primaryButton')
        login_btn.clicked.connect(self.handle_login)

        register_btn = QPushButton('Tạo tài khoản mới')
        register_btn.setObjectName('secondaryButton')
        register_btn.clicked.connect(self.open_register_dialog)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_btn)
        layout.addWidget(register_btn)

        root.addWidget(card)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        user = login(username, password)
        if not user:
            QMessageBox.warning(self, 'Đăng nhập thất bại', 'Tên đăng nhập hoặc mật khẩu không đúng.')
            return

        self.main_window = MainWindow(user)
        self.main_window.show()
        self.close()

    def open_register_dialog(self):
        dialog = RegisterDialog(self)
        dialog.exec()

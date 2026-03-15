from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from config.database import get_connection_settings, test_connection, update_connection_settings
from config.settings import APP_NAME, LOGIN_WINDOW_HEIGHT, LOGIN_WINDOW_WIDTH
from services.auth_service import login
from ui.auth.register_dialog import RegisterDialog
from ui.main_window import MainWindow


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_window = None
        self.setup_ui()
        self.load_db_settings()

    def setup_ui(self):
        self.setWindowTitle(APP_NAME)
        self.setObjectName("loginWindow")
        self.setFixedSize(LOGIN_WINDOW_WIDTH, LOGIN_WINDOW_HEIGHT)

        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(36, 28, 36, 28)

        card = QWidget()
        card.setObjectName("loginCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(12)

        title = QLabel("Đăng nhập hệ thống BCHQS")
        title.setObjectName("loginTitle")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Đăng nhập để quản lý công dân và nhập ngũ")
        subtitle.setObjectName("mutedLabel")
        subtitle.setAlignment(Qt.AlignCenter)

        db_grid = QGridLayout()
        db_grid.setHorizontalSpacing(10)
        db_grid.setVerticalSpacing(10)
        db_grid.setColumnStretch(1, 3)
        db_grid.setColumnStretch(3, 1)

        db_host_label = QLabel("IP / Host DB")
        db_port_label = QLabel("Port DB")

        self.db_host_input = QLineEdit()
        self.db_host_input.setPlaceholderText("127.0.0.1")

        self.db_port_input = QLineEdit()
        self.db_port_input.setPlaceholderText("3306")
        self.db_port_input.setMaximumWidth(120)

        db_grid.addWidget(db_host_label, 0, 0)
        db_grid.addWidget(self.db_host_input, 0, 1)
        db_grid.addWidget(db_port_label, 0, 2)
        db_grid.addWidget(self.db_port_input, 0, 3)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Tên đăng nhập")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mật khẩu")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.returnPressed.connect(self.handle_login)

        login_btn = QPushButton("Đăng nhập")
        login_btn.setObjectName("primaryButton")
        login_btn.clicked.connect(self.handle_login)

        register_btn = QPushButton("Tạo tài khoản mới")
        register_btn.setObjectName("secondaryButton")
        register_btn.clicked.connect(self.open_register_dialog)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(db_grid)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_btn)
        layout.addWidget(register_btn)

        root.addWidget(card)

    def load_db_settings(self):
        settings = get_connection_settings()
        self.db_host_input.setText(str(settings.get("host", "")))
        self.db_port_input.setText(str(settings.get("port", "")))

    def apply_db_settings(self):
        host = self.db_host_input.text().strip()
        port = self.db_port_input.text().strip()
        update_connection_settings(host, port, persist=True)
        test_connection()

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        try:
            self.apply_db_settings()
        except Exception as exc:
            QMessageBox.warning(self, "Lỗi kết nối database", str(exc))
            return

        user, error_message = login(username, password)
        if error_message:
            QMessageBox.warning(self, "Đăng nhập thất bại", error_message)
            return

        self.main_window = MainWindow(user)
        self.main_window.show()
        self.close()

    def open_register_dialog(self):
        try:
            update_connection_settings(
                self.db_host_input.text().strip(),
                self.db_port_input.text().strip(),
                persist=True,
            )
        except Exception as exc:
            QMessageBox.warning(self, "Lỗi cấu hình database", str(exc))
            return

        dialog = RegisterDialog(self)
        dialog.exec()

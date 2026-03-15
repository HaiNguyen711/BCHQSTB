from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QDialog,
    QGridLayout,
    QHBoxLayout,
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


class DatabaseSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        self.setWindowTitle("Thiết lập database")
        self.setFixedSize(420, 260)

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)

        card = QWidget()
        card.setObjectName("loginCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)

        title = QLabel("Thiết lập kết nối database")
        title.setObjectName("loginTitle")
        title.setAlignment(Qt.AlignCenter)

        grid = QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)

        self.db_host_input = QLineEdit()
        self.db_host_input.setPlaceholderText("127.0.0.1")

        self.db_port_input = QLineEdit()
        self.db_port_input.setPlaceholderText("3306")

        self.db_name_input = QLineEdit()
        self.db_name_input.setPlaceholderText("military_citizen_db")

        grid.addWidget(QLabel("IP / Host DB"), 0, 0)
        grid.addWidget(self.db_host_input, 0, 1)
        grid.addWidget(QLabel("Port DB"), 1, 0)
        grid.addWidget(self.db_port_input, 1, 1)
        grid.addWidget(QLabel("DB Name"), 2, 0)
        grid.addWidget(self.db_name_input, 2, 1)

        button_row = QHBoxLayout()
        button_row.addStretch()

        cancel_btn = QPushButton("Hủy")
        cancel_btn.setObjectName("secondaryButton")
        cancel_btn.clicked.connect(self.reject)

        save_btn = QPushButton("Lưu thiết lập")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self.save_settings)

        button_row.addWidget(cancel_btn)
        button_row.addWidget(save_btn)

        layout.addWidget(title)
        layout.addLayout(grid)
        layout.addLayout(button_row)
        root.addWidget(card)

    def load_settings(self):
        settings = get_connection_settings()
        self.db_host_input.setText(str(settings.get("host", "")))
        self.db_port_input.setText(str(settings.get("port", "")))
        self.db_name_input.setText(str(settings.get("database", "")))

    def save_settings(self):
        try:
            update_connection_settings(
                self.db_host_input.text().strip(),
                self.db_port_input.text().strip(),
                self.db_name_input.text().strip(),
                persist=True,
            )
            test_connection()
        except Exception as exc:
            QMessageBox.warning(self, "Lỗi kết nối database", str(exc))
            return

        QMessageBox.information(self, "Thành công", "Đã lưu thiết lập database.")
        self.accept()


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_window = None
        self.setup_ui()
        self.db_settings_shortcut = QShortcut(QKeySequence("Ctrl+Shift+D"), self)
        self.db_settings_shortcut.activated.connect(self.open_db_settings_dialog)

    def setup_ui(self):
        self.setWindowTitle(APP_NAME)
        self.setObjectName("loginWindow")
        self.setFixedSize(LOGIN_WINDOW_WIDTH, LOGIN_WINDOW_HEIGHT)

        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(36, 34, 36, 34)

        card = QWidget()
        card.setObjectName("loginCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(16)

        title = QLabel("Đăng nhập hệ thống BCHQS")
        title.setObjectName("loginTitle")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Đăng nhập để quản lý công dân và nhập ngũ")
        subtitle.setObjectName("mutedLabel")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)

        settings_row = QHBoxLayout()
        settings_row.setContentsMargins(0, 0, 0, 0)
        settings_row.setSpacing(0)

        settings_row.addStretch()

        settings_btn = QPushButton("Thiết lập")
        settings_btn.setObjectName("secondaryButton")
        settings_btn.setFixedWidth(110)
        settings_btn.clicked.connect(self.open_db_settings_dialog)
        settings_row.addWidget(settings_btn)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Tên đăng nhập")
        self.username_input.setMinimumHeight(44)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mật khẩu")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.returnPressed.connect(self.handle_login)
        self.password_input.setMinimumHeight(44)

        login_btn = QPushButton("Đăng nhập")
        login_btn.setObjectName("primaryButton")
        login_btn.clicked.connect(self.handle_login)
        login_btn.setMinimumHeight(44)

        register_btn = QPushButton("Tạo tài khoản mới")
        register_btn.setObjectName("secondaryButton")
        register_btn.clicked.connect(self.open_register_dialog)
        register_btn.setMinimumHeight(44)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(4)
        layout.addLayout(settings_row)
        layout.addSpacing(2)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_btn)
        layout.addWidget(register_btn)
        layout.addStretch()

        root.addWidget(card)

    def apply_db_settings(self):
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

    def open_db_settings_dialog(self):
        dialog = DatabaseSettingsDialog(self)
        dialog.exec()

    def open_register_dialog(self):
        try:
            self.apply_db_settings()
        except Exception as exc:
            QMessageBox.warning(self, "Lỗi cấu hình database", str(exc))
            return

        dialog = RegisterDialog(self)
        dialog.exec()

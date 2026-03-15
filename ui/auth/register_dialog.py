from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout, QWidget

from services.auth_service import create_user


class RegisterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle('Đăng ký tài khoản')
        self.setFixedSize(430, 250)

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)

        card = QWidget()
        card.setObjectName('loginCard')
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)

        title = QLabel('Tạo tài khoản mới')
        title.setObjectName('loginTitle')
        title.setAlignment(Qt.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Tên đăng nhập')

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Mật khẩu')
        self.password_input.setEchoMode(QLineEdit.Password)

        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText('Nhập lại mật khẩu')
        self.confirm_input.setEchoMode(QLineEdit.Password)

        button_row = QHBoxLayout()
        cancel_btn = QPushButton('Hủy')
        cancel_btn.setObjectName('secondaryButton')
        cancel_btn.clicked.connect(self.reject)

        register_btn = QPushButton('Đăng ký')
        register_btn.setObjectName('primaryButton')
        register_btn.clicked.connect(self.register)

        button_row.addStretch()
        button_row.addWidget(cancel_btn)
        button_row.addWidget(register_btn)

        layout.addWidget(title)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.confirm_input)
        layout.addLayout(button_row)

        root.addWidget(card)

    def register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm = self.confirm_input.text().strip()

        if not username or not password or not confirm:
            QMessageBox.warning(self, 'Thiếu thông tin', 'Vui lòng nhập đầy đủ thông tin.')
            return

        if password != confirm:
            QMessageBox.warning(self, 'Sai mật khẩu', 'Mật khẩu nhập lại không khớp.')
            return

        ok, message = create_user(username, password)
        if ok:
            QMessageBox.information(self, 'Thành công', message)
            self.accept()
        else:
            QMessageBox.warning(self, 'Lỗi', message)

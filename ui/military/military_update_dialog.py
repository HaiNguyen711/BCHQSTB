from PySide6.QtWidgets import QComboBox, QDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QTextEdit, QVBoxLayout

from services.military_service import STATUS_OPTIONS, save_military_record


class MilitaryUpdateDialog(QDialog):
    def __init__(self, record, parent=None):
        super().__init__(parent)
        self.record = record or {}
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        self.setWindowTitle('Cập nhật quản lí nhập ngũ')
        self.resize(560, 520)

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 18, 20, 18)
        root.setSpacing(12)

        title = QLabel('Thông tin nhập ngũ')
        title.setObjectName('sectionTitle')

        form = QFormLayout()
        form.setSpacing(12)

        self.cccd = QLineEdit()
        self.cccd.setReadOnly(True)
        self.full_name = QLineEdit()
        self.full_name.setReadOnly(True)

        self.service_status = QComboBox()
        for code, label in STATUS_OPTIONS:
            self.service_status.addItem(label, code)

        self.health_check_date = QLineEdit()
        self.health_check_date.setPlaceholderText('dd-mm-yyyy')
        self.health_result = QLineEdit()
        self.health_result.setPlaceholderText('Ví dụ: Loại 1')
        self.enlistment_date = QLineEdit()
        self.enlistment_date.setPlaceholderText('dd-mm-yyyy')
        self.unit_name = QLineEdit()
        self.position_name = QLineEdit()
        self.note = QTextEdit()
        self.note.setFixedHeight(90)

        form.addRow('CCCD', self.cccd)
        form.addRow('Họ tên', self.full_name)
        form.addRow('Trạng thái', self.service_status)
        form.addRow('Ngày khám', self.health_check_date)
        form.addRow('Kết quả khám', self.health_result)
        form.addRow('Ngày nhập ngũ', self.enlistment_date)
        form.addRow('Đơn vị', self.unit_name)
        form.addRow('Chức vụ', self.position_name)
        form.addRow('Ghi chú', self.note)

        button_row = QHBoxLayout()
        button_row.addStretch()

        cancel_btn = QPushButton('Hủy')
        cancel_btn.setObjectName('secondaryButton')
        cancel_btn.clicked.connect(self.reject)

        save_btn = QPushButton('Lưu')
        save_btn.setObjectName('primaryButton')
        save_btn.clicked.connect(self.save_data)

        button_row.addWidget(cancel_btn)
        button_row.addWidget(save_btn)

        root.addWidget(title)
        root.addLayout(form)
        root.addStretch()
        root.addLayout(button_row)

    def load_data(self):
        self.cccd.setText(self.record.get('cccd', ''))
        self.full_name.setText(self.record.get('full_name', ''))
        self.health_check_date.setText(self.record.get('health_check_date', ''))
        self.health_result.setText(self.record.get('health_result', ''))
        self.enlistment_date.setText(self.record.get('enlistment_date', ''))
        self.unit_name.setText(self.record.get('unit_name', ''))
        self.position_name.setText(self.record.get('position_name', ''))
        self.note.setPlainText(self.record.get('note', ''))

        current_status = self.record.get('service_status', 'CHUA_GOI')
        index = self.service_status.findData(current_status)
        if index >= 0:
            self.service_status.setCurrentIndex(index)

    def save_data(self):
        data = {
            'citizen_cccd': self.cccd.text().strip(),
            'service_status': self.service_status.currentData(),
            'health_check_date': self.health_check_date.text().strip(),
            'health_result': self.health_result.text().strip(),
            'enlistment_date': self.enlistment_date.text().strip(),
            'unit_name': self.unit_name.text().strip(),
            'position_name': self.position_name.text().strip(),
            'note': self.note.toPlainText().strip(),
        }

        ok, message = save_military_record(data)
        if ok:
            QMessageBox.information(self, 'Thành công', message)
            self.accept()
        else:
            QMessageBox.warning(self, 'Lỗi', message)

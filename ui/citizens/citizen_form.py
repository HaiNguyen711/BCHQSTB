from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFileDialog,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from config.settings import CITIZEN_IMAGES_DIR
from services.citizen_service import create_citizen, get_citizen_background, get_citizen_health, save_background, save_health, update_citizen

import os
import shutil


class CitizenForm(QDialog):
    def __init__(self, citizen=None, parent=None):
        super().__init__(parent)
        self.citizen = citizen or {}
        self.photo_source_path = ''
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        self.setWindowTitle('Hồ sơ công dân')
        self.resize(900, 700)

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(12)

        title = QLabel('Thông tin công dân')
        title.setObjectName('sectionTitle')
        root.addWidget(title)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(18)

        self.photo_label = QLabel('Ảnh\n3x4')
        self.photo_label.setObjectName('photoPlaceholder')
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setFixedSize(170, 210)

        photo_button_layout = QVBoxLayout()
        upload_btn = QPushButton('Tải ảnh')
        upload_btn.setObjectName('secondaryButton')
        upload_btn.clicked.connect(self.choose_photo)
        photo_button_layout.addWidget(self.photo_label)
        photo_button_layout.addWidget(upload_btn)
        photo_button_layout.addStretch()

        form_box = QWidget()
        form_layout = QFormLayout(form_box)
        form_layout.setSpacing(12)

        self.cccd = QLineEdit()
        self.full_name = QLineEdit()
        self.date_of_birth = QLineEdit()
        self.date_of_birth.setPlaceholderText('dd-mm-yyyy')

        self.gender = QComboBox()
        self.gender.addItems(['Nam', 'Nữ'])

        self.phone = QLineEdit()
        self.ward = QLineEdit()
        self.address = QLineEdit()
        self.neighborhood = QLineEdit()
        self.education_level = QLineEdit()
        self.occupation = QLineEdit()
        self.religion = QLineEdit()
        self.ethnicity = QLineEdit()

        form_layout.addRow('CCCD', self.cccd)
        form_layout.addRow('Họ tên', self.full_name)
        form_layout.addRow('Ngày sinh', self.date_of_birth)
        form_layout.addRow('Giới tính', self.gender)
        form_layout.addRow('SĐT', self.phone)
        form_layout.addRow('Phường', self.ward)
        form_layout.addRow('Địa chỉ', self.address)
        form_layout.addRow('Khu phố / tổ', self.neighborhood)
        form_layout.addRow('Trình độ học vấn', self.education_level)
        form_layout.addRow('Nghề nghiệp', self.occupation)
        form_layout.addRow('Tôn giáo', self.religion)
        form_layout.addRow('Dân tộc', self.ethnicity)

        top_layout.addLayout(photo_button_layout)
        top_layout.addWidget(form_box, 1)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.build_background_tab(), 'Lý lịch')
        self.tabs.addTab(self.build_health_tab(), 'Sức khỏe')

        button_row = QHBoxLayout()
        button_row.addStretch()

        cancel_btn = QPushButton('Hủy')
        cancel_btn.setObjectName('secondaryButton')
        cancel_btn.clicked.connect(self.reject)

        save_btn = QPushButton('Lưu hồ sơ')
        save_btn.setObjectName('primaryButton')
        save_btn.clicked.connect(self.save_all)

        button_row.addWidget(cancel_btn)
        button_row.addWidget(save_btn)

        root.addLayout(top_layout)
        root.addWidget(self.tabs)
        root.addLayout(button_row)

    def build_background_tab(self):
        tab = QWidget()
        grid = QGridLayout(tab)
        grid.setSpacing(12)

        self.father_name = QLineEdit()
        self.father_phone = QLineEdit()
        self.mother_name = QLineEdit()
        self.mother_phone = QLineEdit()
        self.family_status = QLineEdit()
        self.criminal_record = QLineEdit()
        self.party_union_status = QLineEdit()
        self.notes = QTextEdit()

        grid.addWidget(QLabel('Họ tên cha'), 0, 0)
        grid.addWidget(self.father_name, 0, 1)
        grid.addWidget(QLabel('SĐT cha'), 0, 2)
        grid.addWidget(self.father_phone, 0, 3)

        grid.addWidget(QLabel('Họ tên mẹ'), 1, 0)
        grid.addWidget(self.mother_name, 1, 1)
        grid.addWidget(QLabel('SĐT mẹ'), 1, 2)
        grid.addWidget(self.mother_phone, 1, 3)

        grid.addWidget(QLabel('Tình trạng gia đình'), 2, 0)
        grid.addWidget(self.family_status, 2, 1)
        grid.addWidget(QLabel('Tiền án tiền sự'), 2, 2)
        grid.addWidget(self.criminal_record, 2, 3)

        grid.addWidget(QLabel('Đảng / Đoàn'), 3, 0)
        grid.addWidget(self.party_union_status, 3, 1)
        grid.addWidget(QLabel('Ghi chú'), 4, 0)
        grid.addWidget(self.notes, 4, 1, 1, 3)

        return tab

    def build_health_tab(self):
        tab = QWidget()
        grid = QGridLayout(tab)
        grid.setSpacing(12)

        self.height = QLineEdit()
        self.weight = QLineEdit()
        self.vision = QLineEdit()
        self.blood_pressure = QLineEdit()
        self.health_type = QLineEdit()

        grid.addWidget(QLabel('Chiều cao'), 0, 0)
        grid.addWidget(self.height, 0, 1)
        grid.addWidget(QLabel('Cân nặng'), 0, 2)
        grid.addWidget(self.weight, 0, 3)
        grid.addWidget(QLabel('Thị lực'), 1, 0)
        grid.addWidget(self.vision, 1, 1)
        grid.addWidget(QLabel('Huyết áp'), 1, 2)
        grid.addWidget(self.blood_pressure, 1, 3)
        grid.addWidget(QLabel('Phân loại sức khỏe'), 2, 0)
        grid.addWidget(self.health_type, 2, 1)

        return tab

    def load_data(self):
        if not self.citizen:
            return

        self.cccd.setText(self.citizen.get('cccd', ''))
        self.cccd.setReadOnly(True)
        self.full_name.setText(self.citizen.get('full_name', ''))
        self.date_of_birth.setText(self.citizen.get('date_of_birth', ''))
        self.phone.setText(self.citizen.get('phone', ''))
        self.ward.setText(self.citizen.get('ward', ''))
        self.address.setText(self.citizen.get('address', ''))
        self.neighborhood.setText(self.citizen.get('neighborhood', ''))
        self.education_level.setText(self.citizen.get('education_level', ''))
        self.occupation.setText(self.citizen.get('occupation', ''))
        self.religion.setText(self.citizen.get('religion', ''))
        self.ethnicity.setText(self.citizen.get('ethnicity', ''))

        gender = self.citizen.get('gender', 'Nam')
        index = self.gender.findText(gender)
        if index >= 0:
            self.gender.setCurrentIndex(index)

        bg = get_citizen_background(self.citizen.get('cccd', ''))
        self.father_name.setText(bg.get('father_name', ''))
        self.father_phone.setText(bg.get('father_phone', ''))
        self.mother_name.setText(bg.get('mother_name', ''))
        self.mother_phone.setText(bg.get('mother_phone', ''))
        self.family_status.setText(bg.get('family_status', ''))
        self.criminal_record.setText(bg.get('criminal_record', ''))
        self.party_union_status.setText(bg.get('party_union_status', ''))
        self.notes.setPlainText(bg.get('notes', ''))

        health = get_citizen_health(self.citizen.get('cccd', ''))
        self.height.setText(str(health.get('height', '')))
        self.weight.setText(str(health.get('weight', '')))
        self.vision.setText(health.get('vision', ''))
        self.blood_pressure.setText(health.get('blood_pressure', ''))
        self.health_type.setText(health.get('health_type', ''))

        self.load_photo()

    def load_photo(self):
        cccd = self.cccd.text().strip()
        if not cccd:
            return

        path = os.path.join(CITIZEN_IMAGES_DIR, cccd + '.jpg')
        if os.path.exists(path):
            pixmap = QPixmap(path)
            pixmap = pixmap.scaled(160, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.photo_label.setPixmap(pixmap)
            self.photo_label.setText('')

    def choose_photo(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Chọn ảnh', '', 'Image Files (*.png *.jpg *.jpeg)')
        if path:
            self.photo_source_path = path
            pixmap = QPixmap(path)
            pixmap = pixmap.scaled(160, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.photo_label.setPixmap(pixmap)
            self.photo_label.setText('')

    def save_photo(self, cccd):
        if not self.photo_source_path:
            return

        if not os.path.exists(CITIZEN_IMAGES_DIR):
            os.makedirs(CITIZEN_IMAGES_DIR)

        shutil.copy(self.photo_source_path, os.path.join(CITIZEN_IMAGES_DIR, cccd + '.jpg'))

    def save_all(self):
        citizen_data = {
            'cccd': self.cccd.text().strip(),
            'full_name': self.full_name.text().strip(),
            'date_of_birth': self.date_of_birth.text().strip(),
            'gender': self.gender.currentText(),
            'phone': self.phone.text().strip(),
            'ward': self.ward.text().strip(),
            'address': self.address.text().strip(),
            'neighborhood': self.neighborhood.text().strip(),
            'education_level': self.education_level.text().strip(),
            'occupation': self.occupation.text().strip(),
            'religion': self.religion.text().strip(),
            'ethnicity': self.ethnicity.text().strip(),
        }

        if self.citizen:
            ok, message = update_citizen(citizen_data)
        else:
            ok, message = create_citizen(citizen_data)

        if not ok:
            QMessageBox.warning(self, 'Lỗi', message)
            return

        cccd = citizen_data['cccd']

        background_data = {
            'citizen_cccd': cccd,
            'father_name': self.father_name.text().strip(),
            'father_phone': self.father_phone.text().strip(),
            'mother_name': self.mother_name.text().strip(),
            'mother_phone': self.mother_phone.text().strip(),
            'family_status': self.family_status.text().strip(),
            'criminal_record': self.criminal_record.text().strip(),
            'party_union_status': self.party_union_status.text().strip(),
            'notes': self.notes.toPlainText().strip(),
        }
        save_background(background_data)

        health_data = {
            'citizen_cccd': cccd,
            'height': self.height.text().strip(),
            'weight': self.weight.text().strip(),
            'vision': self.vision.text().strip(),
            'blood_pressure': self.blood_pressure.text().strip(),
            'health_type': self.health_type.text().strip(),
        }
        save_health(health_data)

        self.save_photo(cccd)
        QMessageBox.information(self, 'Thành công', 'Đã lưu hồ sơ công dân.')
        self.accept()

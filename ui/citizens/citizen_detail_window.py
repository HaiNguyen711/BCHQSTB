import os
import shutil

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from config.settings import CITIZEN_IMAGES_DIR
from services.citizen_service import get_citizen_detail, update_citizen_detail


class CitizenDetailWindow(QWidget):
    def __init__(self, cccd):
        super().__init__()
        self.cccd = cccd
        self.photo_path = None
        self.current_avatar_source = None

        self.setWindowTitle("Hồ sơ công dân")
        self.resize(1280, 820)

        self.build_ui()
        self.load_data()

    def build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(18)

        root.addWidget(self.build_profile_sidebar())
        root.addWidget(self.build_main_content(), 1)

    def build_profile_sidebar(self):
        card = QFrame()
        card.setObjectName("profileSidebarCard")
        card.setFixedWidth(290)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignTop)

        # ===== Photo wrapper cố định để tránh text đè lên ảnh =====
        photo_wrap = QWidget()
        photo_wrap.setFixedSize(220, 270)

        photo_wrap_layout = QVBoxLayout(photo_wrap)
        photo_wrap_layout.setContentsMargins(0, 0, 0, 0)
        photo_wrap_layout.setSpacing(0)

        self.avatar = QLabel("Ảnh\ncông dân")
        self.avatar.setObjectName("photoPlaceholder")
        self.avatar.setFixedSize(220, 270)
        self.avatar.setAlignment(Qt.AlignCenter)
        self.avatar.setScaledContents(False)

        photo_wrap_layout.addWidget(self.avatar)

        outer_photo_wrap = QHBoxLayout()
        outer_photo_wrap.setContentsMargins(0, 0, 0, 0)
        outer_photo_wrap.addStretch()
        outer_photo_wrap.addWidget(photo_wrap)
        outer_photo_wrap.addStretch()

        self.name_label = QLabel("")
        self.name_label.setObjectName("profileName")
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setWordWrap(True)

        self.cccd_label = QLabel("")
        self.cccd_label.setObjectName("mutedLabel")
        self.cccd_label.setAlignment(Qt.AlignCenter)

        self.dob_label = QLabel("")
        self.dob_label.setObjectName("mutedLabel")
        self.dob_label.setAlignment(Qt.AlignCenter)

        self.gender_label = QLabel("")
        self.gender_label.setObjectName("mutedLabel")
        self.gender_label.setAlignment(Qt.AlignCenter)

        self.phone_label = QLabel("")
        self.phone_label.setObjectName("mutedLabel")
        self.phone_label.setAlignment(Qt.AlignCenter)

        self.ward_label = QLabel("")
        self.ward_label.setObjectName("mutedLabel")
        self.ward_label.setAlignment(Qt.AlignCenter)

        self.btn_upload = QPushButton("Cập nhật ảnh")
        self.btn_upload.setObjectName("secondaryButton")
        self.btn_upload.clicked.connect(self.upload_photo)

        self.btn_save = QPushButton("Lưu hồ sơ")
        self.btn_save.setObjectName("primaryButton")
        self.btn_save.clicked.connect(self.save_data)

        layout.addLayout(outer_photo_wrap)
        layout.addSpacing(10)
        layout.addWidget(self.name_label)
        layout.addWidget(self.cccd_label)
        layout.addWidget(self.dob_label)
        layout.addWidget(self.gender_label)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.ward_label)
        layout.addSpacing(12)
        layout.addWidget(self.btn_upload)
        layout.addStretch()
        layout.addWidget(self.btn_save)

        return card

    def build_main_content(self):
        wrapper = QWidget()
        wrapper_layout = QVBoxLayout(wrapper)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.setSpacing(12)

        title = QLabel("Thông tin hồ sơ công dân")
        title.setObjectName("pageTitle")
        wrapper_layout.addWidget(title)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.build_personal_tab(), "Thông tin cá nhân")
        self.tabs.addTab(self.build_family_tab(), "Gia đình")
        self.tabs.addTab(self.build_health_tab(), "Sức khỏe")

        wrapper_layout.addWidget(self.tabs)
        return wrapper

    def build_personal_tab(self):
        container = QWidget()
        outer = QVBoxLayout(container)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(12)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(6, 6, 6, 6)
        page_layout.setSpacing(14)

        card = QFrame()
        card.setObjectName("infoCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(12)

        section = QLabel("Thông tin cá nhân")
        section.setObjectName("sectionTitle")
        card_layout.addWidget(section)

        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(12)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(3, 1)

        self.address = QLineEdit()
        self.neighborhood = QLineEdit()
        self.education_level = QLineEdit()
        self.occupation = QLineEdit()
        self.religion = QLineEdit()
        self.ethnicity = QLineEdit()

        self.birth_registration_place = QLineEdit()
        self.hometown = QLineEdit()
        self.nationality = QLineEdit()
        self.family_permanent_residence = QLineEdit()
        self.current_residence = QLineEdit()
        self.family_component = QLineEdit()
        self.general_education_level = QLineEdit()
        self.training_level = QLineEdit()
        self.training_major = QLineEdit()
        self.party_join_date = QLineEdit()
        self.union_join_date = QLineEdit()
        self.workplace_or_school = QLineEdit()

        fields = [
            ("Địa chỉ", self.address, "Khu phố / tổ", self.neighborhood),
            ("Trình độ học vấn", self.education_level, "Nghề nghiệp", self.occupation),
            ("Tôn giáo", self.religion, "Dân tộc", self.ethnicity),
            ("Nơi đăng kí khai sinh", self.birth_registration_place, "Quê quán", self.hometown),
            ("Quốc tịch", self.nationality, "Nơi thường trú gia đình", self.family_permanent_residence),
            ("Nơi ở hiện tại", self.current_residence, "Thành phần gia đình", self.family_component),
            ("Trình độ GD phổ thông", self.general_education_level, "Trình độ đào tạo", self.training_level),
            ("Chuyên ngành đào tạo", self.training_major, "Ngày vào Đảng", self.party_join_date),
            ("Ngày vào Đoàn", self.union_join_date, "Nơi làm việc / học tập", self.workplace_or_school),
        ]

        for row, (label1, widget1, label2, widget2) in enumerate(fields):
            grid.addWidget(self.make_field_label(label1), row, 0)
            grid.addWidget(widget1, row, 1)
            grid.addWidget(self.make_field_label(label2), row, 2)
            grid.addWidget(widget2, row, 3)

        card_layout.addLayout(grid)
        page_layout.addWidget(card)
        page_layout.addStretch()

        scroll.setWidget(page)
        outer.addWidget(scroll)
        return container

    def build_family_tab(self):
        container = QWidget()
        outer = QVBoxLayout(container)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(12)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(6, 6, 6, 6)
        page_layout.setSpacing(14)

        parent_card = QFrame()
        parent_card.setObjectName("infoCard")
        parent_layout = QVBoxLayout(parent_card)
        parent_layout.setContentsMargins(16, 16, 16, 16)
        parent_layout.setSpacing(12)

        parent_title = QLabel("Thông tin cha mẹ")
        parent_title.setObjectName("sectionTitle")
        parent_layout.addWidget(parent_title)

        self.father_name = QLineEdit()
        self.father_birth_date = QLineEdit()
        self.father_phone = QLineEdit()
        self.father_status = QLineEdit()

        self.mother_name = QLineEdit()
        self.mother_birth_date = QLineEdit()
        self.mother_phone = QLineEdit()
        self.mother_status = QLineEdit()

        parent_grid = QGridLayout()
        parent_grid.setHorizontalSpacing(16)
        parent_grid.setVerticalSpacing(12)
        parent_grid.setColumnStretch(1, 1)
        parent_grid.setColumnStretch(3, 1)

        parent_fields = [
            ("Họ tên cha", self.father_name, "Ngày sinh cha", self.father_birth_date),
            ("SĐT cha", self.father_phone, "Tình trạng cha", self.father_status),
            ("Họ tên mẹ", self.mother_name, "Ngày sinh mẹ", self.mother_birth_date),
            ("SĐT mẹ", self.mother_phone, "Tình trạng mẹ", self.mother_status),
        ]

        for row, (label1, widget1, label2, widget2) in enumerate(parent_fields):
            parent_grid.addWidget(self.make_field_label(label1), row, 0)
            parent_grid.addWidget(widget1, row, 1)
            parent_grid.addWidget(self.make_field_label(label2), row, 2)
            parent_grid.addWidget(widget2, row, 3)

        parent_layout.addLayout(parent_grid)

        family_card = QFrame()
        family_card.setObjectName("infoCard")
        family_layout = QVBoxLayout(family_card)
        family_layout.setContentsMargins(16, 16, 16, 16)
        family_layout.setSpacing(12)

        family_title = QLabel("Tình hình gia đình")
        family_title.setObjectName("sectionTitle")
        family_layout.addWidget(family_title)

        self.family_status = QLineEdit()
        self.criminal_record = QLineEdit()
        self.party_union_status = QLineEdit()
        self.spouse_info = QLineEdit()
        self.children_info = QLineEdit()
        self.total_male_children = QLineEdit()
        self.total_female_children = QLineEdit()
        self.birth_order = QLineEdit()

        family_grid = QGridLayout()
        family_grid.setHorizontalSpacing(16)
        family_grid.setVerticalSpacing(12)
        family_grid.setColumnStretch(1, 1)
        family_grid.setColumnStretch(3, 1)

        family_fields = [
            ("Tình trạng gia đình", self.family_status, "Tiền án tiền sự", self.criminal_record),
            ("Đảng / Đoàn", self.party_union_status, "Thông tin vợ/chồng", self.spouse_info),
            ("Thông tin con cái", self.children_info, "Số con trai trong gia đình", self.total_male_children),
            ("Số con gái trong gia đình", self.total_female_children, "Bản thân là con thứ", self.birth_order),
        ]

        for row, (label1, widget1, label2, widget2) in enumerate(family_fields):
            family_grid.addWidget(self.make_field_label(label1), row, 0)
            family_grid.addWidget(widget1, row, 1)
            family_grid.addWidget(self.make_field_label(label2), row, 2)
            family_grid.addWidget(widget2, row, 3)

        family_layout.addLayout(family_grid)

        page_layout.addWidget(parent_card)
        page_layout.addWidget(family_card)
        page_layout.addStretch()

        scroll.setWidget(page)
        outer.addWidget(scroll)
        return container

    def build_health_tab(self):
        container = QWidget()
        outer = QVBoxLayout(container)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(12)

        card = QFrame()
        card.setObjectName("infoCard")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(12)

        section = QLabel("Thông tin sức khỏe")
        section.setObjectName("sectionTitle")
        card_layout.addWidget(section)

        self.height = QLineEdit()
        self.weight = QLineEdit()
        self.vision = QLineEdit()
        self.blood_pressure = QLineEdit()
        self.health_type = QLineEdit()

        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(12)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(3, 1)

        health_fields = [
            ("Chiều cao", self.height, "Cân nặng", self.weight),
            ("Thị lực", self.vision, "Huyết áp", self.blood_pressure),
            ("Phân loại sức khỏe", self.health_type, "", None),
        ]

        for row, (label1, widget1, label2, widget2) in enumerate(health_fields):
            grid.addWidget(self.make_field_label(label1), row, 0)
            grid.addWidget(widget1, row, 1)

            if widget2 is not None:
                grid.addWidget(self.make_field_label(label2), row, 2)
                grid.addWidget(widget2, row, 3)

        card_layout.addLayout(grid)
        outer.addWidget(card)
        outer.addStretch()

        return container

    def make_field_label(self, text):
        label = QLabel(text)
        label.setObjectName("detailFieldLabel")
        return label

    def load_data(self):
        data = get_citizen_detail(self.cccd)
        if not data:
            return

        citizen = data.get("citizen") or {}
        background = data.get("background") or {}
        health = data.get("health") or {}

        self.name_label.setText(citizen.get("full_name", ""))
        self.cccd_label.setText(f"CCCD: {citizen.get('cccd', '')}")
        self.dob_label.setText(f"Ngày sinh: {citizen.get('date_of_birth', '')}")
        self.gender_label.setText(f"Giới tính: {citizen.get('gender', '')}")
        self.phone_label.setText(f"SĐT: {citizen.get('phone', '')}")
        self.ward_label.setText(f"Phường: {citizen.get('ward', '')}")

        self.address.setText(citizen.get("address", "") or "")
        self.neighborhood.setText(citizen.get("neighborhood", "") or "")
        self.education_level.setText(citizen.get("education_level", "") or "")
        self.occupation.setText(citizen.get("occupation", "") or "")
        self.religion.setText(citizen.get("religion", "") or "")
        self.ethnicity.setText(citizen.get("ethnicity", "") or "")

        self.birth_registration_place.setText(background.get("birth_registration_place", "") or "")
        self.hometown.setText(background.get("hometown", "") or "")
        self.nationality.setText(background.get("nationality", "") or "")
        self.family_permanent_residence.setText(background.get("family_permanent_residence", "") or "")
        self.current_residence.setText(background.get("current_residence", "") or "")
        self.family_component.setText(background.get("family_component", "") or "")
        self.general_education_level.setText(background.get("general_education_level", "") or "")
        self.training_level.setText(background.get("training_level", "") or "")
        self.training_major.setText(background.get("training_major", "") or "")
        self.party_join_date.setText(background.get("party_join_date", "") or "")
        self.union_join_date.setText(background.get("union_join_date", "") or "")
        self.workplace_or_school.setText(background.get("workplace_or_school", "") or "")

        self.father_name.setText(background.get("father_name", "") or "")
        self.father_birth_date.setText(background.get("father_birth_date", "") or "")
        self.father_phone.setText(background.get("father_phone", "") or "")
        self.father_status.setText(background.get("father_status", "") or "")

        self.mother_name.setText(background.get("mother_name", "") or "")
        self.mother_birth_date.setText(background.get("mother_birth_date", "") or "")
        self.mother_phone.setText(background.get("mother_phone", "") or "")
        self.mother_status.setText(background.get("mother_status", "") or "")

        self.family_status.setText(background.get("family_status", "") or "")
        self.criminal_record.setText(background.get("criminal_record", "") or "")
        self.party_union_status.setText(background.get("party_union_status", "") or "")
        self.spouse_info.setText(background.get("spouse_info", "") or "")
        self.children_info.setText(background.get("children_info", "") or "")
        self.total_male_children.setText(str(background.get("total_male_children", "") or ""))
        self.total_female_children.setText(str(background.get("total_female_children", "") or ""))
        self.birth_order.setText(background.get("birth_order", "") or "")

        self.height.setText(str(health.get("height", "") or ""))
        self.weight.setText(str(health.get("weight", "") or ""))
        self.vision.setText(health.get("vision", "") or "")
        self.blood_pressure.setText(health.get("blood_pressure", "") or "")
        self.health_type.setText(health.get("health_type", "") or "")

        photo_path = citizen.get("photo_path", "") or ""
        if photo_path and os.path.exists(photo_path):
            self.current_avatar_source = photo_path
            self.update_avatar_display()

    def update_avatar_display(self):
        if not self.current_avatar_source or not os.path.exists(self.current_avatar_source):
            return

        pixmap = QPixmap(self.current_avatar_source)
        if pixmap.isNull():
            return

        target_width = self.avatar.width() - 8
        target_height = self.avatar.height() - 8

        scaled = pixmap.scaled(
            target_width,
            target_height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.avatar.setPixmap(scaled)
        self.avatar.setText("")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.current_avatar_source:
            self.update_avatar_display()

    def upload_photo(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Chọn ảnh",
            "",
            "Image Files (*.png *.jpg *.jpeg)"
        )

        if not file_path:
            return

        if not os.path.exists(CITIZEN_IMAGES_DIR):
            os.makedirs(CITIZEN_IMAGES_DIR)

        new_path = os.path.join(CITIZEN_IMAGES_DIR, f"{self.cccd}.jpg")
        shutil.copy(file_path, new_path)

        self.photo_path = new_path
        self.current_avatar_source = new_path
        self.update_avatar_display()

    def save_data(self):
        data = {
            "cccd": self.cccd,
            "address": self.address.text().strip(),
            "neighborhood": self.neighborhood.text().strip(),
            "education_level": self.education_level.text().strip(),
            "occupation": self.occupation.text().strip(),
            "religion": self.religion.text().strip(),
            "ethnicity": self.ethnicity.text().strip(),

            "birth_registration_place": self.birth_registration_place.text().strip(),
            "hometown": self.hometown.text().strip(),
            "nationality": self.nationality.text().strip(),
            "family_permanent_residence": self.family_permanent_residence.text().strip(),
            "current_residence": self.current_residence.text().strip(),
            "family_component": self.family_component.text().strip(),
            "general_education_level": self.general_education_level.text().strip(),
            "training_level": self.training_level.text().strip(),
            "training_major": self.training_major.text().strip(),
            "party_join_date": self.party_join_date.text().strip(),
            "union_join_date": self.union_join_date.text().strip(),
            "workplace_or_school": self.workplace_or_school.text().strip(),

            "father_name": self.father_name.text().strip(),
            "father_birth_date": self.father_birth_date.text().strip(),
            "father_phone": self.father_phone.text().strip(),
            "father_status": self.father_status.text().strip(),

            "mother_name": self.mother_name.text().strip(),
            "mother_birth_date": self.mother_birth_date.text().strip(),
            "mother_phone": self.mother_phone.text().strip(),
            "mother_status": self.mother_status.text().strip(),

            "family_status": self.family_status.text().strip(),
            "criminal_record": self.criminal_record.text().strip(),
            "party_union_status": self.party_union_status.text().strip(),
            "spouse_info": self.spouse_info.text().strip(),
            "children_info": self.children_info.text().strip(),
            "total_male_children": self.total_male_children.text().strip(),
            "total_female_children": self.total_female_children.text().strip(),
            "birth_order": self.birth_order.text().strip(),

            "height": self.height.text().strip(),
            "weight": self.weight.text().strip(),
            "vision": self.vision.text().strip(),
            "blood_pressure": self.blood_pressure.text().strip(),
            "health_type": self.health_type.text().strip(),

            "photo_path": self.photo_path,
        }

        ok = update_citizen_detail(data)

        if ok:
            QMessageBox.information(self, "Thành công", "Đã lưu hồ sơ.")
        else:
            QMessageBox.warning(self, "Lỗi", "Không thể lưu hồ sơ.")
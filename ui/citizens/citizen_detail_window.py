import os
import shutil

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from config.settings import CITIZEN_IMAGES_DIR
from services.citizen_service import get_citizen_detail, update_citizen_detail


class CitizenDetailWindow(QWidget):
    PERSONAL_STAGE_ORDER = [
        "Thơ ấu",
        "Cấp 1",
        "Cấp 2",
        "Cấp 3",
        "Đại học",
        "Sau đại học",
    ]

    def __init__(self, cccd):
        super().__init__()
        self.cccd = cccd
        self.photo_path = None
        self.current_avatar_source = None
        self.sibling_rows = []
        self.personal_stage_rows = []

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

        personal_situation_card = QFrame()
        personal_situation_card.setObjectName("infoCard")
        personal_situation_layout = QVBoxLayout(personal_situation_card)
        personal_situation_layout.setContentsMargins(16, 16, 16, 16)
        personal_situation_layout.setSpacing(12)

        personal_situation_header = QHBoxLayout()
        personal_situation_header.setContentsMargins(0, 0, 0, 0)

        personal_situation_title = QLabel("Lý lịch bản thân")
        personal_situation_title.setObjectName("sectionTitle")
        self.add_personal_stage_button = QPushButton("Thêm cấp")
        self.add_personal_stage_button.setObjectName("secondaryButton")
        self.add_personal_stage_button.clicked.connect(self.add_next_personal_stage)

        personal_situation_header.addWidget(personal_situation_title)
        personal_situation_header.addStretch()
        personal_situation_header.addWidget(self.add_personal_stage_button)
        personal_situation_layout.addLayout(personal_situation_header)

        self.personal_stage_hint = QLabel(
            "Thêm các giai đoạn theo thứ tự: Thơ ấu -> Cấp 1 -> Cấp 2 -> Cấp 3 -> Đại học -> Sau đại học"
        )
        self.personal_stage_hint.setObjectName("detailFieldLabel")
        self.personal_stage_hint.setWordWrap(True)
        personal_situation_layout.addWidget(self.personal_stage_hint)

        self.personal_stage_container = QWidget()
        self.personal_stage_layout = QVBoxLayout(self.personal_stage_container)
        self.personal_stage_layout.setContentsMargins(0, 0, 0, 0)
        self.personal_stage_layout.setSpacing(10)
        personal_situation_layout.addWidget(self.personal_stage_container)

        page_layout.addWidget(personal_situation_card)
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
        self.father_occupation = QLineEdit()
        self.father_phone = QLineEdit()
        self.father_status = QComboBox()
        self.mother_name = QLineEdit()
        self.mother_birth_date = QLineEdit()
        self.mother_occupation = QLineEdit()
        self.mother_phone = QLineEdit()
        self.mother_status = QComboBox()
        self.father_history_before_1975 = QTextEdit()
        self.father_history_after_1975 = QTextEdit()
        self.mother_history_before_1975 = QTextEdit()
        self.mother_history_after_1975 = QTextEdit()

        self.father_status.addItems(["Sống", "Chết"])
        self.mother_status.addItems(["Sống", "Chết"])

        self.father_history_before_1975.setPlaceholderText("Thông tin lý lịch của cha trước năm 1975")
        self.father_history_after_1975.setPlaceholderText("Thông tin lý lịch của cha sau năm 1975")
        self.mother_history_before_1975.setPlaceholderText("Thông tin lý lịch của mẹ trước năm 1975")
        self.mother_history_after_1975.setPlaceholderText("Thông tin lý lịch của mẹ sau năm 1975")

        for editor in (
            self.father_history_before_1975,
            self.father_history_after_1975,
            self.mother_history_before_1975,
            self.mother_history_after_1975,
        ):
            editor.setMinimumHeight(90)

        parent_columns = QHBoxLayout()
        parent_columns.setContentsMargins(0, 0, 0, 0)
        parent_columns.setSpacing(16)

        father_card = self.build_parent_side(
            "Thông tin cha",
            [
                ("Họ tên cha", self.father_name),
                ("Ngày sinh cha", self.father_birth_date),
                ("Nghề nghiệp cha", self.father_occupation),
                ("SĐT cha", self.father_phone),
                ("Tình trạng cha", self.father_status),
                ("Lý lịch cha trước 1975", self.father_history_before_1975),
                ("Lý lịch cha sau 1975", self.father_history_after_1975),
            ],
        )
        mother_card = self.build_parent_side(
            "Thông tin mẹ",
            [
                ("Họ tên mẹ", self.mother_name),
                ("Ngày sinh mẹ", self.mother_birth_date),
                ("Nghề nghiệp mẹ", self.mother_occupation),
                ("SĐT mẹ", self.mother_phone),
                ("Tình trạng mẹ", self.mother_status),
                ("Lý lịch mẹ trước 1975", self.mother_history_before_1975),
                ("Lý lịch mẹ sau 1975", self.mother_history_after_1975),
            ],
        )

        parent_columns.addWidget(father_card, 1)
        parent_columns.addWidget(mother_card, 1)
        parent_layout.addLayout(parent_columns)

        family_card = QFrame()
        family_card.setObjectName("infoCard")
        family_layout = QVBoxLayout(family_card)
        family_layout.setContentsMargins(16, 16, 16, 16)
        family_layout.setSpacing(12)

        family_header = QHBoxLayout()
        family_header.setContentsMargins(0, 0, 0, 0)

        family_title = QLabel("Tình hình gia đình")
        family_title.setObjectName("sectionTitle")
        self.add_sibling_button = QPushButton("Thêm anh/chị/em")
        self.add_sibling_button.setObjectName("secondaryButton")
        self.add_sibling_button.clicked.connect(self.add_sibling_row)

        family_header.addWidget(family_title)
        family_header.addStretch()
        family_header.addWidget(self.add_sibling_button)
        family_layout.addLayout(family_header)

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
        family_layout.addWidget(self.build_siblings_section())

        page_layout.addWidget(parent_card)
        page_layout.addWidget(family_card)
        page_layout.addStretch()

        scroll.setWidget(page)
        outer.addWidget(scroll)
        return container

    def build_parent_side(self, title_text, fields):
        card = QFrame()
        card.setObjectName("infoCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        title = QLabel(title_text)
        title.setObjectName("detailFieldLabel")
        layout.addWidget(title)

        for label_text, widget in fields:
            layout.addWidget(self.make_field_label(label_text))
            layout.addWidget(widget)

        layout.addStretch()
        return card

    def build_siblings_section(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 4, 0, 0)
        layout.setSpacing(10)

        title = QLabel("Thông tin anh chị em")
        title.setObjectName("detailFieldLabel")
        layout.addWidget(title)

        self.siblings_container = QWidget()
        self.siblings_layout = QVBoxLayout(self.siblings_container)
        self.siblings_layout.setContentsMargins(0, 0, 0, 0)
        self.siblings_layout.setSpacing(10)
        layout.addWidget(self.siblings_container)

        return container

    def add_sibling_row(self, sibling_data=None):
        sibling_data = sibling_data or {}

        row_card = QFrame()
        row_card.setObjectName("infoCard")
        row_card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        row_layout = QVBoxLayout(row_card)
        row_layout.setContentsMargins(14, 14, 14, 14)
        row_layout.setSpacing(10)

        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)

        title = QLabel(f"Anh/chị/em {len(self.sibling_rows) + 1}")
        title.setObjectName("detailFieldLabel")

        remove_button = QPushButton("Xóa")
        remove_button.setObjectName("secondaryButton")

        header.addWidget(title)
        header.addStretch()
        header.addWidget(remove_button)
        row_layout.addLayout(header)

        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(10)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(3, 1)

        name_input = QLineEdit()
        birth_date_input = QLineEdit()
        occupation_input = QLineEdit()
        workplace_input = QLineEdit()
        relation_input = QComboBox()

        birth_date_input.setPlaceholderText("dd-mm-yyyy")
        relation_input.addItems(["Anh trai", "Chị gái", "Em trai", "Em gái"])
        name_input.setText(sibling_data.get("full_name", "") or "")
        birth_date_input.setText(sibling_data.get("date_of_birth", "") or "")
        occupation_input.setText(sibling_data.get("occupation", "") or "")
        workplace_input.setText(sibling_data.get("workplace", "") or "")
        self.set_combo_text(relation_input, sibling_data.get("relation", "") or "Anh trai")

        fields = [
            ("Quan hệ", relation_input, "Ngày sinh", birth_date_input),
            ("Họ tên", name_input, "Nghề nghiệp", occupation_input),
            ("Nơi công tác", workplace_input, "", None),
        ]

        for row, (label1, widget1, label2, widget2) in enumerate(fields):
            grid.addWidget(self.make_field_label(label1), row, 0)
            grid.addWidget(widget1, row, 1)
            if widget2 is not None:
                grid.addWidget(self.make_field_label(label2), row, 2)
                grid.addWidget(widget2, row, 3)

        row_layout.addLayout(grid)
        self.siblings_layout.addWidget(row_card)

        row_info = {
            "card": row_card,
            "title": title,
            "relation": relation_input,
            "full_name": name_input,
            "date_of_birth": birth_date_input,
            "occupation": occupation_input,
            "workplace": workplace_input,
            "remove_button": remove_button,
        }
        self.sibling_rows.append(row_info)
        remove_button.clicked.connect(lambda: self.remove_sibling_row(row_info))
        self.update_sibling_titles()

    def remove_sibling_row(self, row_info):
        if row_info not in self.sibling_rows:
            return

        self.sibling_rows.remove(row_info)
        row_info["card"].deleteLater()
        self.update_sibling_titles()

    def update_sibling_titles(self):
        for index, row_info in enumerate(self.sibling_rows, start=1):
            row_info["title"].setText(f"Anh/chị/em {index}")

    def clear_sibling_rows(self):
        for row_info in self.sibling_rows:
            row_info["card"].deleteLater()
        self.sibling_rows = []

    def load_siblings(self, siblings):
        self.clear_sibling_rows()
        for sibling in siblings:
            self.add_sibling_row(sibling)

    def collect_siblings(self):
        siblings = []
        for row_info in self.sibling_rows:
            sibling = {
                "relation": row_info["relation"].currentText().strip(),
                "full_name": row_info["full_name"].text().strip(),
                "date_of_birth": row_info["date_of_birth"].text().strip(),
                "occupation": row_info["occupation"].text().strip(),
                "workplace": row_info["workplace"].text().strip(),
            }
            if any(sibling.values()):
                siblings.append(sibling)
        return siblings

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

    def set_combo_text(self, combo_box, value):
        index = combo_box.findText(value)
        if index >= 0:
            combo_box.setCurrentIndex(index)

    def add_next_personal_stage(self, stage_data=None):
        stage_name = None
        if stage_data:
            stage_name = stage_data.get("stage", "")
        elif len(self.personal_stage_rows) < len(self.PERSONAL_STAGE_ORDER):
            stage_name = self.PERSONAL_STAGE_ORDER[len(self.personal_stage_rows)]

        if not stage_name:
            return

        existing_stages = {row["stage"] for row in self.personal_stage_rows}
        if stage_name in existing_stages:
            return

        row_card = QFrame()
        row_card.setObjectName("infoCard")
        row_card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        title = QLabel(stage_name)
        title.setObjectName("detailFieldLabel")
        title.setFixedWidth(110)

        row_layout = QHBoxLayout(row_card)
        row_layout.setContentsMargins(14, 10, 14, 10)
        row_layout.setSpacing(10)

        remove_button = QPushButton("Xóa")
        remove_button.setObjectName("secondaryButton")
        remove_button.setFixedWidth(52)

        content_input = QLineEdit()
        content_input.setPlaceholderText(
            f"Ghi ngắn gọn tình hình ở giai đoạn {stage_name.lower()}"
        )
        content_input.setText(stage_data.get("content", "") if stage_data else "")

        row_layout.addWidget(title)
        row_layout.addWidget(content_input, 1)
        row_layout.addWidget(remove_button)

        self.personal_stage_layout.addWidget(row_card)

        row_info = {
            "card": row_card,
            "stage": stage_name,
            "title": title,
            "content": content_input,
            "remove_button": remove_button,
        }
        self.personal_stage_rows.append(row_info)
        self.personal_stage_rows.sort(
            key=lambda row: self.PERSONAL_STAGE_ORDER.index(row["stage"])
        )
        self.rebuild_personal_stage_layout()
        remove_button.clicked.connect(lambda: self.remove_personal_stage(row_info))
        self.update_personal_stage_button_state()

    def remove_personal_stage(self, row_info):
        if row_info not in self.personal_stage_rows:
            return

        self.personal_stage_rows.remove(row_info)
        row_info["card"].deleteLater()
        self.update_personal_stage_button_state()

    def rebuild_personal_stage_layout(self):
        for row_info in self.personal_stage_rows:
            self.personal_stage_layout.removeWidget(row_info["card"])
        for row_info in self.personal_stage_rows:
            self.personal_stage_layout.addWidget(row_info["card"])

    def clear_personal_stages(self):
        for row_info in self.personal_stage_rows:
            row_info["card"].deleteLater()
        self.personal_stage_rows = []
        self.update_personal_stage_button_state()

    def load_personal_stages(self, stages):
        self.clear_personal_stages()
        if isinstance(stages, list):
            ordered = sorted(
                stages,
                key=lambda item: self.PERSONAL_STAGE_ORDER.index(item.get("stage"))
                if item.get("stage") in self.PERSONAL_STAGE_ORDER else len(self.PERSONAL_STAGE_ORDER),
            )
            for stage in ordered:
                self.add_next_personal_stage(stage)
        self.update_personal_stage_button_state()

    def collect_personal_stages(self):
        stages = []
        for row_info in self.personal_stage_rows:
            content = row_info["content"].text().strip()
            if content:
                stages.append(
                    {
                        "stage": row_info["stage"],
                        "content": content,
                    }
                )
        return stages

    def update_personal_stage_button_state(self):
        self.add_personal_stage_button.setEnabled(
            len(self.personal_stage_rows) < len(self.PERSONAL_STAGE_ORDER)
        )

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
        self.load_personal_stages(background.get("personal_situation_stages", []) or [])

        self.father_name.setText(background.get("father_name", "") or "")
        self.father_birth_date.setText(background.get("father_birth_date", "") or "")
        self.father_occupation.setText(background.get("father_occupation", "") or "")
        self.father_phone.setText(background.get("father_phone", "") or "")
        self.set_combo_text(self.father_status, background.get("father_status", "") or "Sống")

        self.mother_name.setText(background.get("mother_name", "") or "")
        self.mother_birth_date.setText(background.get("mother_birth_date", "") or "")
        self.mother_occupation.setText(background.get("mother_occupation", "") or "")
        self.mother_phone.setText(background.get("mother_phone", "") or "")
        self.set_combo_text(self.mother_status, background.get("mother_status", "") or "Sống")
        self.father_history_before_1975.setPlainText(background.get("father_history_before_1975", "") or "")
        self.father_history_after_1975.setPlainText(background.get("father_history_after_1975", "") or "")
        self.mother_history_before_1975.setPlainText(background.get("mother_history_before_1975", "") or "")
        self.mother_history_after_1975.setPlainText(background.get("mother_history_after_1975", "") or "")

        self.family_status.setText(background.get("family_status", "") or "")
        self.criminal_record.setText(background.get("criminal_record", "") or "")
        self.party_union_status.setText(background.get("party_union_status", "") or "")
        self.spouse_info.setText(background.get("spouse_info", "") or "")
        self.children_info.setText(background.get("children_info", "") or "")
        self.total_male_children.setText(str(background.get("total_male_children", "") or ""))
        self.total_female_children.setText(str(background.get("total_female_children", "") or ""))
        self.birth_order.setText(background.get("birth_order", "") or "")
        self.load_siblings(background.get("siblings", []) or [])

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
            Qt.SmoothTransformation,
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
            "Image Files (*.png *.jpg *.jpeg)",
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
            "personal_situation": self.collect_personal_stages(),
            "father_name": self.father_name.text().strip(),
            "father_birth_date": self.father_birth_date.text().strip(),
            "father_occupation": self.father_occupation.text().strip(),
            "father_phone": self.father_phone.text().strip(),
            "father_status": self.father_status.currentText().strip(),
            "mother_name": self.mother_name.text().strip(),
            "mother_birth_date": self.mother_birth_date.text().strip(),
            "mother_occupation": self.mother_occupation.text().strip(),
            "mother_phone": self.mother_phone.text().strip(),
            "mother_status": self.mother_status.currentText().strip(),
            "father_history_before_1975": self.father_history_before_1975.toPlainText().strip(),
            "father_history_after_1975": self.father_history_after_1975.toPlainText().strip(),
            "mother_history_before_1975": self.mother_history_before_1975.toPlainText().strip(),
            "mother_history_after_1975": self.mother_history_after_1975.toPlainText().strip(),
            "family_status": self.family_status.text().strip(),
            "criminal_record": self.criminal_record.text().strip(),
            "party_union_status": self.party_union_status.text().strip(),
            "spouse_info": self.spouse_info.text().strip(),
            "children_info": self.children_info.text().strip(),
            "total_male_children": self.total_male_children.text().strip(),
            "total_female_children": self.total_female_children.text().strip(),
            "birth_order": self.birth_order.text().strip(),
            "siblings": self.collect_siblings(),
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

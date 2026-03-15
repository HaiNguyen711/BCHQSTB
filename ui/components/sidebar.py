import qtawesome as qta
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout


class Sidebar(QFrame):
    citizen_clicked = Signal()
    military_clicked = Signal()
    stats_clicked = Signal()
    report_clicked = Signal()

    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setup_ui()

    def setup_ui(self):
        username = 'admin'
        if isinstance(self.user, dict):
            username = self.user.get('username', 'admin')
        elif self.user:
            username = str(self.user)

        self.setObjectName('sidebar')
        self.setFixedWidth(250)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 20, 18, 20)
        layout.setSpacing(10)

        logo = QLabel('BCHQS')
        logo.setObjectName('sidebarLogo')
        logo.setAlignment(Qt.AlignCenter)

        sub_logo = QLabel('QUẢN LÝ CÔNG DÂN TRẤN BIÊN')
        sub_logo.setObjectName('sidebarSubLogo')
        sub_logo.setAlignment(Qt.AlignCenter)
        sub_logo.setWordWrap(True)

        layout.addWidget(logo)
        layout.addWidget(sub_logo)
        layout.addSpacing(16)

        self.btn_citizen = QPushButton(qta.icon('fa5s.users'), '  Quản lý công dân')
        self.btn_military = QPushButton(qta.icon('fa5s.shield-alt'), '  Quản lí nhập ngũ')
        self.btn_stats = QPushButton(qta.icon('fa5s.chart-bar'), '  Thống kê')
        self.btn_report = QPushButton(qta.icon('fa5s.file-alt'), '  Hồ sơ báo cáo')

        layout.addWidget(self.btn_citizen)
        layout.addWidget(self.btn_military)
        layout.addWidget(self.btn_stats)
        layout.addWidget(self.btn_report)
        layout.addStretch()

        self.user_card = QLabel('Người dùng hiện tại\n' + username)
        self.user_card.setObjectName('sidebarUserCard')
        self.user_card.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.user_card)

        self.btn_citizen.clicked.connect(self.citizen_clicked.emit)
        self.btn_military.clicked.connect(self.military_clicked.emit)
        self.btn_stats.clicked.connect(self.stats_clicked.emit)
        self.btn_report.clicked.connect(self.report_clicked.emit)

        self.set_active('citizen')

    def set_citizen_count(self, count):
        self.btn_citizen.setText(f'  Quản lý công dân ({count})')

    def set_active(self, page_name):
        buttons = {
            'citizen': self.btn_citizen,
            'military': self.btn_military,
            'stats': self.btn_stats,
            'report': self.btn_report,
        }

        for key, button in buttons.items():
            if key == page_name:
                button.setObjectName('menuButtonActive')
            else:
                button.setObjectName('menuButton')
            button.style().unpolish(button)
            button.style().polish(button)
            button.update()

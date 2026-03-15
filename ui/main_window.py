from PySide6.QtWidgets import QHBoxLayout, QLabel, QMainWindow, QStackedWidget, QVBoxLayout, QWidget

from config.settings import APP_NAME, MAIN_WINDOW_HEIGHT, MAIN_WINDOW_WIDTH
from ui.citizens.citizen_management_widget import CitizenManagementWidget
from ui.components.sidebar import Sidebar
from ui.military.military_management_widget import MilitaryManagementWidget


class PlaceholderPage(QWidget):
    def __init__(self, title, subtitle):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)

        title_label = QLabel(title)
        title_label.setObjectName('pageTitle')

        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName('mutedLabel')

        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addStretch()


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(APP_NAME)
        self.resize(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)

        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.sidebar = Sidebar(self.user)
        self.sidebar.citizen_clicked.connect(self.show_citizen_page)
        self.sidebar.military_clicked.connect(self.show_military_page)
        self.sidebar.stats_clicked.connect(self.show_stats_page)
        self.sidebar.report_clicked.connect(self.show_report_page)

        self.stack = QStackedWidget()

        self.citizen_page = CitizenManagementWidget(self)
        self.military_page = MilitaryManagementWidget(self)
        self.stats_page = PlaceholderPage('Thống kê', 'Module thống kê sẽ phát triển tiếp trên nền này.')
        self.report_page = PlaceholderPage('Hồ sơ báo cáo', 'Module hồ sơ báo cáo sẽ phát triển tiếp trên nền này.')

        self.stack.addWidget(self.citizen_page)
        self.stack.addWidget(self.military_page)
        self.stack.addWidget(self.stats_page)
        self.stack.addWidget(self.report_page)

        root.addWidget(self.sidebar)
        root.addWidget(self.stack, 1)

        self.show_citizen_page()

    def show_citizen_page(self):
        self.stack.setCurrentWidget(self.citizen_page)
        self.sidebar.set_active('citizen')

    def show_military_page(self):
        self.military_page.load_data()
        self.stack.setCurrentWidget(self.military_page)
        self.sidebar.set_active('military')

    def show_stats_page(self):
        self.stack.setCurrentWidget(self.stats_page)
        self.sidebar.set_active('stats')

    def show_report_page(self):
        self.stack.setCurrentWidget(self.report_page)
        self.sidebar.set_active('report')

    def refresh_related_pages(self):
        self.citizen_page.load_data()
        self.military_page.load_data()

from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from services.stats_service import get_dashboard_stats


class StatsDashboardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        page = QWidget()
        self.page_layout = QVBoxLayout(page)
        self.page_layout.setContentsMargins(24, 24, 24, 24)
        self.page_layout.setSpacing(16)

        title = QLabel('Thống kê')
        title.setObjectName('pageTitle')

        subtitle = QLabel('Tổng quan nhanh về công dân và tình hình nhập ngũ trên toàn hệ thống.')
        subtitle.setObjectName('mutedLabel')
        subtitle.setWordWrap(True)

        self.summary_grid = QGridLayout()
        self.summary_grid.setHorizontalSpacing(16)
        self.summary_grid.setVerticalSpacing(16)

        self.total_card = self.build_stat_card('Tổng công dân')
        self.eligible_card = self.build_stat_card('Độ tuổi 18-27')
        self.male_card = self.build_stat_card('Nam')
        self.female_card = self.build_stat_card('Nữ')

        self.summary_grid.addWidget(self.total_card['card'], 0, 0)
        self.summary_grid.addWidget(self.eligible_card['card'], 0, 1)
        self.summary_grid.addWidget(self.male_card['card'], 1, 0)
        self.summary_grid.addWidget(self.female_card['card'], 1, 1)

        self.breakdown_grid = QGridLayout()
        self.breakdown_grid.setHorizontalSpacing(16)
        self.breakdown_grid.setVerticalSpacing(16)

        self.status_card = self.build_list_card('Trạng thái nhập ngũ')
        self.ward_card = self.build_list_card('Phường nhiều công dân')

        self.breakdown_grid.addWidget(self.status_card['card'], 0, 0)
        self.breakdown_grid.addWidget(self.ward_card['card'], 0, 1)

        self.page_layout.addWidget(title)
        self.page_layout.addWidget(subtitle)
        self.page_layout.addLayout(self.summary_grid)
        self.page_layout.addLayout(self.breakdown_grid)
        self.page_layout.addStretch()

        scroll.setWidget(page)
        root.addWidget(scroll)

    def build_stat_card(self, label_text):
        card = QFrame()
        card.setObjectName('infoCard')

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(8)

        value = QLabel('0')
        value.setObjectName('statValue')

        label = QLabel(label_text)
        label.setObjectName('statCaption')
        label.setWordWrap(True)

        layout.addWidget(value)
        layout.addWidget(label)

        return {
            'card': card,
            'value': value,
            'label': label,
        }

    def build_list_card(self, title_text):
        card = QFrame()
        card.setObjectName('infoCard')

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        title = QLabel(title_text)
        title.setObjectName('sectionTitle')

        content = QVBoxLayout()
        content.setContentsMargins(0, 6, 0, 0)
        content.setSpacing(8)

        layout.addWidget(title)
        layout.addLayout(content)
        layout.addStretch()

        return {
            'card': card,
            'content': content,
        }

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            child_layout = item.layout()
            if widget is not None:
                widget.deleteLater()
            elif child_layout is not None:
                self.clear_layout(child_layout)

    def add_list_row(self, layout, label_text, count_value):
        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(8)

        label = QLabel(label_text)
        label.setObjectName('detailFieldLabel')
        label.setMinimumWidth(120)

        count = QLabel(str(count_value))
        count.setObjectName('statMiniValue')

        row_layout.addWidget(label)
        row_layout.addStretch()
        row_layout.addWidget(count)
        layout.addWidget(row)

    def load_data(self):
        stats = get_dashboard_stats()

        self.total_card['value'].setText(str(stats.get('total_citizens', 0)))
        self.eligible_card['value'].setText(str(stats.get('eligible_age_count', 0)))
        self.male_card['value'].setText(str(stats.get('male_count', 0)))
        self.female_card['value'].setText(str(stats.get('female_count', 0)))

        self.clear_layout(self.status_card['content'])
        for item in stats.get('military_status_counts', []):
            self.add_list_row(self.status_card['content'], item.get('label', ''), item.get('count', 0))

        self.clear_layout(self.ward_card['content'])
        for item in stats.get('ward_counts', []):
            self.add_list_row(self.ward_card['content'], item.get('label', ''), item.get('count', 0))

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from services.military_service import (
    STATUS_LABELS,
    STATUS_OPTIONS,
    get_all_military_records,
    get_military_record,
    search_military_records,
)
from ui.components.header import Header
from ui.components.table_widget import MilitaryTable
from ui.military.military_update_dialog import MilitaryUpdateDialog


class MilitaryManagementWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.status_tables = {}
        self.records_by_status = {}
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self.header = Header(
            'Quản lí nhập ngũ',
            'Tìm theo tên, CCCD, đơn vị...',
            self.perform_search,
            'Cập nhật trạng thái',
            self.open_selected_record,
        )

        self.status_tabs = QTabWidget()
        for status_code, status_label in STATUS_OPTIONS:
            table = MilitaryTable()
            self.status_tables[status_code] = table
            self.status_tabs.addTab(table, status_label)

        layout.addWidget(self.header)
        layout.addWidget(self.status_tabs)

    def make_item(self, text, alignment):
        item = QTableWidgetItem(str(text))
        item.setTextAlignment(alignment)
        return item

    def get_active_table(self):
        status_code = self.status_tabs.currentWidget().property('status_code')
        if status_code:
            return self.status_tables.get(status_code)
        return self.status_tabs.currentWidget()

    def build_action_widget(self, row):
        action_widget = QWidget()
        action_layout = QHBoxLayout(action_widget)
        action_layout.setContentsMargins(0, 0, 0, 0)
        action_layout.setSpacing(6)

        edit_btn = QPushButton('Sửa')
        edit_btn.setObjectName('secondaryButton')
        edit_btn.clicked.connect(lambda _, data=row: self.open_dialog(data))
        action_layout.addWidget(edit_btn)
        action_layout.addStretch()
        return action_widget

    def populate_tables(self, rows):
        self.records_by_status = {code: [] for code, _ in STATUS_OPTIONS}
        for row in rows:
            status_code = row.get('service_status') or 'CHUA_GOI'
            self.records_by_status.setdefault(status_code, []).append(row)

        for index, (status_code, status_label) in enumerate(STATUS_OPTIONS):
            table = self.status_tables[status_code]
            table.setProperty('status_code', status_code)
            status_rows = self.records_by_status.get(status_code, [])
            table.setRowCount(len(status_rows))

            for row_index, row in enumerate(status_rows):
                table.setItem(row_index, 0, self.make_item(row.get('cccd', ''), Qt.AlignCenter))
                table.setItem(row_index, 1, self.make_item(row.get('full_name', ''), Qt.AlignVCenter | Qt.AlignLeft))
                table.setItem(row_index, 2, self.make_item(row.get('date_of_birth', ''), Qt.AlignCenter))
                table.setItem(row_index, 3, self.make_item(row.get('service_status_label', ''), Qt.AlignCenter))
                table.setItem(row_index, 4, self.make_item(row.get('enlistment_date', ''), Qt.AlignCenter))
                table.setItem(row_index, 5, self.make_item(row.get('unit_name', ''), Qt.AlignVCenter | Qt.AlignLeft))
                table.setCellWidget(row_index, 6, self.build_action_widget(row))

            self.status_tabs.setTabText(index, f'{status_label} ({len(status_rows)})')

    def load_data(self):
        self.populate_tables(get_all_military_records())

    def refresh(self):
        self.load_data()

    def perform_search(self):
        keyword = self.header.search.text().strip()
        self.populate_tables(search_military_records(keyword))

    def open_dialog(self, record):
        dialog = MilitaryUpdateDialog(record, self)
        if dialog.exec():
            self.load_data()

    def open_selected_record(self):
        table = self.status_tabs.currentWidget()
        row = table.currentRow()
        if row < 0:
            return

        cccd_item = table.item(row, 0)
        if not cccd_item:
            return

        record = get_military_record(cccd_item.text())
        if record:
            self.open_dialog(record)

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QTableWidgetItem, QVBoxLayout, QWidget

from services.military_service import get_all_military_records, get_military_record, search_military_records
from ui.components.header import Header
from ui.components.table_widget import MilitaryTable
from ui.military.military_update_dialog import MilitaryUpdateDialog


class MilitaryManagementWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
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
            'Cập nhật nhập ngũ',
            self.open_selected_record,
        )

        self.table = MilitaryTable()

        layout.addWidget(self.header)
        layout.addWidget(self.table)

    def populate_table(self, rows):
        self.table.setRowCount(len(rows))

        for row_index, row in enumerate(rows):
            self.table.setItem(row_index, 0, self.make_item(row.get('cccd', ''), Qt.AlignCenter))
            self.table.setItem(row_index, 1, self.make_item(row.get('full_name', ''), Qt.AlignVCenter | Qt.AlignLeft))
            self.table.setItem(row_index, 2, self.make_item(row.get('date_of_birth', ''), Qt.AlignCenter))
            self.table.setItem(row_index, 3, self.make_item(row.get('service_status_label', ''), Qt.AlignCenter))
            self.table.setItem(row_index, 4, self.make_item(row.get('enlistment_date', ''), Qt.AlignCenter))
            self.table.setItem(row_index, 5, self.make_item(row.get('unit_name', ''), Qt.AlignVCenter | Qt.AlignLeft))

            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(6)

            edit_btn = QPushButton('✏')
            edit_btn.clicked.connect(lambda _, data=row: self.open_dialog(data))
            action_layout.addWidget(edit_btn)

            self.table.setCellWidget(row_index, 6, action_widget)

    def make_item(self, text, alignment):
        item = QTableWidgetItem(str(text))
        item.setTextAlignment(alignment)
        return item

    def load_data(self):
        self.populate_table(get_all_military_records())

    def refresh(self):
        self.load_data()

    def perform_search(self):
        keyword = self.header.search.text().strip()
        self.populate_table(search_military_records(keyword))

    def open_dialog(self, record):
        dialog = MilitaryUpdateDialog(record, self)
        if dialog.exec():
            self.load_data()

    def open_selected_record(self):
        row = self.table.currentRow()
        if row < 0:
            return

        cccd_item = self.table.item(row, 0)
        if not cccd_item:
            return

        record = get_military_record(cccd_item.text())
        if record:
            self.open_dialog(record)

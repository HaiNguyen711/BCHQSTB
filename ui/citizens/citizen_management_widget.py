from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QMessageBox, QPushButton, QTableWidgetItem, QVBoxLayout, QWidget

from services.citizen_import_service import import_citizens_from_excel
from services.citizen_service import delete_citizen, get_all_citizens, search_citizens
from ui.citizens.citizen_detail_window import CitizenDetailWindow
from ui.citizens.citizen_form import CitizenForm
from ui.components.header import Header
from ui.components.table_widget import CitizenTable


class CitizenManagementWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.detail_windows = []
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self.header = Header(
            'Quản lý công dân',
            'Tìm theo tên hoặc CCCD...',
            self.perform_search,
            'Thêm công dân',
            self.open_add_form,
        )

        action_row = QHBoxLayout()
        action_row.setContentsMargins(0, 0, 0, 0)
        action_row.addStretch()

        self.import_button = QPushButton('Import from Excel')
        self.import_button.setObjectName('secondaryButton')
        self.import_button.clicked.connect(self.import_from_excel)
        action_row.addWidget(self.import_button)

        self.table = CitizenTable()
        self.table.itemDoubleClicked.connect(self.open_detail)

        layout.addWidget(self.header)
        layout.addLayout(action_row)
        layout.addWidget(self.table)

    def populate_table(self, citizens):
        self.table.setRowCount(len(citizens))

        for row, citizen in enumerate(citizens):
            self.table.setItem(row, 0, self.make_item(citizen.get('cccd', ''), Qt.AlignCenter))
            self.table.setItem(row, 1, self.make_item(citizen.get('full_name', ''), Qt.AlignVCenter | Qt.AlignLeft))
            self.table.setItem(row, 2, self.make_item(citizen.get('date_of_birth', ''), Qt.AlignCenter))
            self.table.setItem(row, 3, self.make_item(citizen.get('gender', ''), Qt.AlignCenter))
            self.table.setItem(row, 4, self.make_item(citizen.get('phone', ''), Qt.AlignCenter))
            self.table.setItem(row, 5, self.make_item(citizen.get('ward', ''), Qt.AlignVCenter | Qt.AlignLeft))

            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(0)

            delete_btn = QPushButton('🗑')
            delete_btn.clicked.connect(lambda _, data=citizen: self.remove_citizen(data))

            action_layout.addWidget(delete_btn)
            action_layout.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(row, 6, action_widget)

    def make_item(self, text, alignment):
        item = QTableWidgetItem(str(text))
        item.setTextAlignment(alignment)
        return item

    def load_data(self):
        self.populate_table(get_all_citizens())

    def refresh(self):
        self.load_data()

    def perform_search(self):
        keyword = self.header.search.text().strip()
        self.populate_table(search_citizens(keyword))

    def open_add_form(self):
        dialog = CitizenForm(parent=self)
        if dialog.exec():
            self.load_data()
            self.parent().refresh_related_pages()

    def remove_citizen(self, citizen):
        reply = QMessageBox.question(self, 'Xác nhận', 'Bạn có chắc muốn xóa công dân này?')
        if reply != QMessageBox.Yes:
            return

        ok, message = delete_citizen(citizen.get('cccd', ''))
        if ok:
            self.load_data()
            self.parent().refresh_related_pages()
        else:
            QMessageBox.warning(self, 'Lỗi', message)

    def open_detail(self, item):
        row = item.row()
        cccd_item = self.table.item(row, 0)
        if not cccd_item:
            return

        detail_window = CitizenDetailWindow(cccd_item.text())
        detail_window.show()
        self.detail_windows.append(detail_window)

    def import_from_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            'Chọn file Excel',
            '',
            'Excel Files (*.xlsx)',
        )
        if not file_path:
            return

        ok, message = import_citizens_from_excel(file_path)
        if ok:
            QMessageBox.information(self, 'Thành công', message)
            self.load_data()
            self.parent().refresh_related_pages()
        else:
            QMessageBox.warning(self, 'Lỗi', message)

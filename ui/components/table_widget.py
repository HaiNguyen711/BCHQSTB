from PySide6.QtCore import Qt
from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QTableWidget


class BaseTable(QTableWidget):
    def __init__(self, headers):
        super().__init__()
        self.headers = headers
        self.setup_ui()

    def setup_ui(self):
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(self.headers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(False)
        self.setShowGrid(False)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(44)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.setObjectName('citizenTable')


class CitizenTable(BaseTable):
    def __init__(self):
        BaseTable.__init__(self, ['CCCD', 'Họ tên', 'Ngày sinh', 'Giới tính', 'SĐT', 'Phường', ''])


class MilitaryTable(BaseTable):
    def __init__(self):
        BaseTable.__init__(self, ['CCCD', 'Họ tên', 'Ngày sinh', 'Trạng thái', 'Ngày nhập ngũ', 'Đơn vị', ''])

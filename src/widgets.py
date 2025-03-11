# widgets.py 定义了一些常用的控件，包括标签页容器、结果表格等。
from PyQt5.QtWidgets import QTabWidget, QTableWidget, QHeaderView

class CalculationTabWidget(QTabWidget):
    """统一的计算标签页容器"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabPosition(QTabWidget.North)
        self.setMovable(False)

class ResultTable(QTableWidget):
    """统一结果表格"""
    def __init__(self, headers, parent=None):
        super().__init__(parent)
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setVisible(False)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
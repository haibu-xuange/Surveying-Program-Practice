# style.py
MAIN_STYLESHEET = """
/* 主窗口样式 */
QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #0a1f3d, stop:1 #1a3b5a);
    border-radius: 10px;
}

/* 通用控件样式 */
QWidget {
    background: transparent;
    font-family: '微软雅黑';
}

/* 分组框样式 */
QGroupBox {
    background: rgba(16, 32, 64, 200);
    border: 2px solid #3a6da3;
    border-radius: 8px;
    color: #a0d0ff;
    font-size: 14px;
    padding: 15px;
    margin: 10px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 0 5px;
    color: #b0e0ff;
    font-size: 15px;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

/* 输入控件样式 */
QLineEdit, QTextEdit, QComboBox {
    background: rgba(16, 32, 64, 0.6);
    border: 1px solid #3a6da3;
    border-radius: 4px;
    padding: 6px;
    color: #a0f0ff;
    selection-background-color: #3a6da3;
}

QComboBox QAbstractItemView {
    background: rgba(16, 32, 64, 0.8);
    color: #a0f0ff;
    selection-background-color: #3a6da3;
}

/* 按钮样式 */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #3a6da3, stop:1 #2a4d7a);
    border: 1px solid #4d8fcc;
    border-radius: 5px;
    color: #d0f0ff;
    padding: 8px 15px;
    font-weight: bold;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #4d8fcc, stop:1 #3a6da3);
}

QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #2a4d7a, stop:1 #3a6da3);
}

/* 标签页样式 */
QTabWidget::pane {
    border: none;
    background: rgba(255, 255, 255, 0.05);
}

QTabBar::tab {
    background: rgba(255, 255, 255, 0.1);
    color: #bdc3c7;
    padding: 8px 20px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background: rgba(52, 152, 219, 0.7);
    color: white;
}

/* 文本编辑框样式 */
QTextEdit {
    background-color: rgba(0, 0, 0, 0.15);
    border-radius: 6px;
    font-family: 'Consolas';
    color: #a0f0ff;
}

/* 标签样式 */
QLabel {
    color: #b0f0ff;
    font-weight: semi-bold;
}

/* 滚动条样式 */
QScrollBar:vertical {
    background: rgba(255, 255, 255, 0.05);
    width: 10px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: rgba(52, 152, 219, 0.6);
    min-height: 20px;
    border-radius: 4px;
}

/* 菜单栏样式 */
QMenuBar {
    background: rgba(16, 32, 64, 0.9);
    padding: 4px;
    border-bottom: 1px solid #3a6da3;
}

QMenuBar::item {
    color: #a0d0ff;
    padding: 4px 10px;
    background: transparent;
}

QMenuBar::item:selected {
    background: rgba(58, 109, 163, 0.6);
    border-radius: 4px;
}

QMenu {
    background: rgba(16, 32, 64, 0.9);
    border: 1px solid #3a6da3;
    color: #a0d0ff;
}

QMenu::item {
    padding: 6px 25px;
}

QMenu::item:selected {
    background: rgba(58, 109, 163, 0.6);
}

/* 下拉框样式增强 */
QComboBox {
    color: #a0f0ff;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;
    border-left: 1px solid #3a6da3;
}

QComboBox::down-arrow {
    image: url(icons/down_arrow.svg);
}

/* 数值输入框增强 */
QDoubleSpinBox, QSpinBox {
    background: rgba(16, 32, 64, 0.6);
    border: 1px solid #4d8fcc;
    border-radius: 4px;
    color: #a0f0ff;
    padding: 5px;
}

QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
    width: 20px;
    background: rgba(58, 109, 163, 0.3);
}

QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {
    background: rgba(58, 109, 163, 0.5);
}

/* 表格样式 */
QTableWidget {
    background: rgba(16, 32, 64, 0.5);
    border: 1px solid #3a6da3;
    gridline-color: #2a4d7a;
    font-family: Consolas;
}

QHeaderView::section {
    background-color: #1a3b5a;
    color: #8ab4f8;
    padding: 6px;
    border: none;
}

QTableWidget::item {
    padding: 4px;
    border-bottom: 1px solid #2a4d7a;
}

/* 结果标签样式 */
QLabel#result_label {
    font-size: 16px;
    color: #4d8fcc;
    padding: 10px;
    border: 1px solid #3a6da3;
    border-radius: 4px;
}

/* 按钮组布局 */
QHBoxLayout > QPushButton {
    margin-right: 10px;
    min-width: 100px;
}

QTableWidget#curvature_table {
    background: rgba(16, 32, 64, 0.6);
    border: 1px solid #3a6da3;
    gridline-color: #2a4d7a;
    font-family: Consolas;
    color: #a0f0ff;
}

QTableWidget#curvature_table QTableCornerButton::section {
    background-color: #1a3b5a;
    border: 1px solid #3a6da3;
}

QTableWidget#curvature_table::item {
    padding: 6px;
    border-bottom: 1px solid #2a4d7a;
    color: #a0f0ff;
}

QTableWidget#curvature_table::item:selected {
    background-color: #3a6da3;
    color: #ffffff;
}

/* 子午线弧长结果样式 */
QLabel#arc_result_value {
    font-size: 18px;
    font-weight: bold;
    color: #4d8fcc;
    background: rgba(16, 32, 64, 0.6);
    border: 1px solid #3a6da3;
    border-radius: 6px;
    padding: 10px;
    margin-top: 10px;
    min-width: 200px;
    text-align: center;
}

/* 子午线收敛角表格样式 */
QTableWidget#gamma_table {
    background: rgba(16, 32, 64, 0.6);
    border: 1px solid #3a6da3;
    gridline-color: #2a4d7a;
    font-family: Consolas;
    color: #a0f0ff;
}

QTableWidget#gamma_table::item {
    padding: 6px;
    border-bottom: 1px solid #2a4d7a;
    color: #a0f0ff;
}

QTableWidget#gamma_table::item:selected {
    background-color: #3a6da3;
    color: #ffffff;
}


/* GPS拟合表格样式 */
QTableWidget#gps_table {
    background: rgba(16, 32, 64, 0.6);
    border: 1px solid #3a6da3;
    gridline-color: #2a4d7a;
    font-family: Consolas;
    color: #a0f0ff;
}

QTableWidget#gps_table::item {
    padding: 6px;
    border-bottom: 1px solid #2a4d7a;
}

QTableWidget#gps_table::item:selected {
    background-color: #3a6da3;
    color: #ffffff;
}

/* 已知点颜色 */
QTableWidget#gps_table::item[type="known"] {
    color: #a0f0ff;  /* 冰蓝色 */
}

/* 未知点颜色 */
QTableWidget#gps_table::item[type="unknown"] {
    color: #ff6666;  /* 红色 */
}

/* 计算结果颜色 */
QTableWidget#gps_table::item[type="calculated"] {
    color: #4d8fcc;  /* 亮蓝色 */
}


"""
# style.py 用于设置程序的样式
MAIN_STYLESHEET = """
QMainWindow {
    background-color: rgba(13, 40, 62, 0.95);
    border-radius: 8px;
}

QWidget {
    background: transparent;
    font-family: '微软雅黑';
}

QGroupBox {
    background-color: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(52, 152, 219, 0.3);
    border-radius: 8px;
    margin-top: 10px;
    padding: 15px 5px 5px 5px;
    color: #ecf0f1;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 0 5px;
    color: #3498db;
}

QLineEdit, QTextEdit, QComboBox {
    background-color: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(52, 152, 219, 0.3);
    border-radius: 4px;
    padding: 6px;
    color: #ecf0f1;
    selection-background-color: #2980b9;
}

QPushButton {
    background-color: rgba(52, 152, 219, 0.7);
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    color: white;
    min-width: 80px;
}

QPushButton:hover {
    background-color: rgba(41, 128, 185, 0.8);
}

QPushButton:pressed {
    background-color: rgba(21, 67, 96, 0.9);
}

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

QTextEdit {
    background-color: rgba(0, 0, 0, 0.15);
    border-radius: 6px;
    font-family: 'Consolas';
}

QLabel {
    color: #bdc3c7;
}

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
"""
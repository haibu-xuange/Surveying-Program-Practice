# style.py
MAIN_STYLESHEET = """
QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #0a1f3d, stop:1 #1a3b5a);
    border-radius: 10px;
}

QWidget {
    background: transparent;
    font-family: '微软雅黑';
}

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
    color: #a0f0ff;
}

QLabel {
    color: #b0f0ff;
    font-weight: semi-bold;
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
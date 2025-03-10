# ui_module.py
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QFileDialog, QComboBox,
                             QTextEdit, QMessageBox, QGroupBox)
from PyQt5.QtGui import QIcon
from coordinate_converter import CoordinateConverter
from file_io import FileHandler
from style import MAIN_STYLESHEET


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("坐标转换系统")
        self.setGeometry(100, 100, 900, 700)
        self.setWindowIcon(QIcon('icon.png'))
        
        self.converter = CoordinateConverter()
        self.file_handler = FileHandler()
        
        self.init_ui()
        self.setStyleSheet(MAIN_STYLESHEET)

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        
        # 左侧布局
        left_layout = QVBoxLayout()
        
        # 创建两个转换组
        blh_group = self.create_blh_group()
        site_group = self.create_site_group()
        
        left_layout.addWidget(blh_group)
        left_layout.addWidget(site_group)
        left_layout.setStretch(0, 1)
        left_layout.setStretch(1, 1)
        
        # 右侧布局
        right_layout = QVBoxLayout()
        self.convert_btn = QPushButton("开始转换", clicked=self.on_convert)
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        
        right_layout.addWidget(self.convert_btn)
        right_layout.addWidget(self.output_text)
        
        main_layout.addLayout(left_layout, 60)
        main_layout.addLayout(right_layout, 40)
        
        self.setCentralWidget(main_widget)

    def create_blh_group(self):
        group = QGroupBox("空间直角转大地坐标")
        layout = QVBoxLayout()
        
        # 文件选择
        file_group = QGroupBox("文件操作")
        file_layout = QHBoxLayout()
        self.blh_file_edit = QLineEdit()
        btn_browse = QPushButton("浏览", clicked=lambda: self.select_file(self.blh_file_edit))
        file_layout.addWidget(QLabel("输入文件:"))
        file_layout.addWidget(self.blh_file_edit)
        file_layout.addWidget(btn_browse)
        file_group.setLayout(file_layout)
        
        # 参数选择
        param_group = QGroupBox("转换参数")
        param_layout = QHBoxLayout()
        self.ellipsoid_combo = QComboBox()
        self.ellipsoid_combo.addItems(["克拉索夫斯基", "WGS-84", "CGCS2000"])
        param_layout.addWidget(QLabel("选择椭球:"))
        param_layout.addWidget(self.ellipsoid_combo)
        param_group.setLayout(param_layout)
        
        layout.addWidget(file_group)
        layout.addWidget(param_group)
        group.setLayout(layout)
        return group

    def create_site_group(self):
        group = QGroupBox("空间直角转站心坐标")
        layout = QVBoxLayout()
        
        # 文件操作组（改为水平布局）
        file_group = QGroupBox("文件操作")
        file_layout = QVBoxLayout()  # 外层用垂直布局包含两个水平部分
        
        # 第一行：文件选择（水平布局）
        file_select_layout = QHBoxLayout()  # 新增水平布局
        self.site_file_edit = QLineEdit()
        btn_browse = QPushButton("浏览", clicked=lambda: self.select_file(self.site_file_edit))
        file_select_layout.addWidget(QLabel("输入文件:"))  # 按用户要求保持标签
        file_select_layout.addWidget(self.site_file_edit)
        file_select_layout.addWidget(btn_browse)
        
        # 第二行：站点输入（保持原有水平布局）
        site_point_layout = QHBoxLayout()
        self.site_point_edit = QLineEdit()
        site_point_layout.addWidget(QLabel("站心点号:"))
        site_point_layout.addWidget(self.site_point_edit)
        
        # 将两个水平布局加入垂直布局
        file_layout.addLayout(file_select_layout)
        file_layout.addLayout(site_point_layout)
        file_group.setLayout(file_layout)
        
        layout.addWidget(file_group)
        group.setLayout(layout)
        return group
    
    def select_file(self, edit_widget):
        filename, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "Text Files (*.txt)")
        if filename:
            edit_widget.setText(filename)

    def on_convert(self):
        output = []
        
        # 处理大地坐标转换
        if self.blh_file_edit.text():
            try:
                data = self.file_handler.read_xyz_file(self.blh_file_edit.text())
                ellipsoid = self.ellipsoid_combo.currentText()
                results = []
                for point in data:
                    blh = self.converter.xyz_to_blh(
                        point['X'], point['Y'], point['Z'], ellipsoid
                    )
                    results.append({
                        'Point': point['Point'],
                        'B': blh[0],
                        'L': blh[1],
                        'H': blh[2]
                    })
                blh_output = self.file_handler.format_blh_output(results)
                # 先将转换结果添加到输出
                output.append("=== 大地坐标转换结果 ===")
                output.append(blh_output)
                # 保存文件并添加路径信息
                saved_file = self.file_handler.save_blh_file(blh_output)
                output.append(f"文件已保存：{saved_file}")
            except Exception as e:
                output.append(f"大地坐标转换错误: {str(e)}")
        
        # 处理站心坐标转换
        if self.site_file_edit.text() and self.site_point_edit.text():
            try:
                data = self.file_handler.read_xyz_file(self.site_file_edit.text())
                site_point = self.site_point_edit.text().strip()
                site_data = next((p for p in data if p['Point'] == site_point), None)
                if not site_data:
                    raise ValueError(f"找不到站心点 {site_point}")
                results = self.converter.xyz_to_site_coords(data, site_data)
                site_output = self.file_handler.format_site_output(results)
                # 先将转换结果添加到输出
                output.append("\n=== 站心坐标转换结果 ===")
                output.append(site_output)
                # 保存文件并添加路径信息
                saved_file = self.file_handler.save_site_file(site_output)
                output.append(f"文件已保存：{saved_file}")
            except Exception as e:
                output.append(f"\n站心坐标转换错误: {str(e)}")
        
        # 显示结果
        self.output_text.setText('\n'.join(output))
        if any("错误" in line for line in output):
            QMessageBox.critical(self, "错误", "转换过程中发生错误，请查看输出详情！")
        elif output:
            QMessageBox.information(self, "成功", "转换完成，结果已保存！")
        else:
            QMessageBox.warning(self, "警告", "请先选择输入文件并设置参数！")
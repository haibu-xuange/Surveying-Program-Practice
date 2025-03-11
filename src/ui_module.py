# ui_module.py
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QFileDialog, QComboBox,
                             QTextEdit, QMessageBox, QGroupBox, QFormLayout,
                             QDoubleSpinBox, QTableWidgetItem, QStackedWidget, QAction,
                             QTableWidget, QHeaderView)
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt
from coordinate_converter import CoordinateConverter
from file_io import FileHandler
from style import MAIN_STYLESHEET
from widgets import CalculationTabWidget, ResultTable
from ellipsoid_calculator import EllipsoidCalculator
from ellipsoid_params import ELLIPSOID_PARAMS
from gps_fitting import GPSFitter


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("坐标转换系统")
        self.setGeometry(100, 100, 900, 700)
        self.setWindowIcon(QIcon('icon.png'))        
        self.converter = CoordinateConverter()
        self.file_handler = FileHandler()
        self.calculator = EllipsoidCalculator()
        self.ellipsoids = ELLIPSOID_PARAMS
        
        # 创建主界面容器
        self.stacked_widget = QStackedWidget()
        self.init_menu()
        self.init_pages()
        
        self.setCentralWidget(self.stacked_widget)
        self.setStyleSheet(MAIN_STYLESHEET)

    def init_menu(self):
        """初始化导航菜单栏"""
        menu_bar = self.menuBar()
        
        # 坐标转换菜单
        coord_menu = menu_bar.addMenu("功能导航")
        self.coord_action = QAction("坐标转换", self)
        self.coord_action.triggered.connect(lambda: self.switch_page(0))
        coord_menu.addAction(self.coord_action)
        
        # 椭球计算菜单
        self.ellipsoid_action = QAction("椭球计算", self)
        self.ellipsoid_action.triggered.connect(lambda: self.switch_page(1))
        coord_menu.addAction(self.ellipsoid_action)
        
        # GPS拟合菜单
        self.gps_action = QAction("GPS拟合", self)
        self.gps_action.triggered.connect(lambda: self.switch_page(2))
        coord_menu.addAction(self.gps_action)
        

        # 预留功能菜单
        self.reserved_action = QAction("预留功能", self)
        self.reserved_action.triggered.connect(lambda: self.switch_page(3))
        coord_menu.addAction(self.reserved_action)

    def init_pages(self):
        """初始化各功能页面"""
        # 坐标转换页面（原有功能）
        self.coord_page = self.create_coordinate_page()
        self.stacked_widget.addWidget(self.coord_page)
        
        # 椭球计算页面（新增功能）
        self.ellipsoid_page = self.create_ellipsoid_page()
        self.stacked_widget.addWidget(self.ellipsoid_page)

        # GPS拟合页面（新增功能）
        self.gps_page = self.create_gps_page()
        self.stacked_widget.addWidget(self.gps_page)
        
        # 预留页面
        self.reserved_page = QWidget()
        self.reserved_page.setLayout(QVBoxLayout())
        self.reserved_page.layout().addWidget(QLabel("功能开发中，敬请期待..."))
        self.stacked_widget.addWidget(self.reserved_page)


############ 坐标转换 ############
    def create_coordinate_page(self):
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
        return main_widget
    
    def create_ellipsoid_page(self):
        """创建椭球计算页面（新增功能）"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # 子标签容器（保持原有椭球计算界面）
        sub_tabs = CalculationTabWidget()
        sub_tabs.addTab(self.create_curvature_ui(), "曲率半径")
        sub_tabs.addTab(self.create_arc_ui(), "子午线弧长")
        sub_tabs.addTab(self.create_convergence_ui(), "收敛角计算")
        
        layout.addWidget(sub_tabs)
        return page

    def switch_page(self, index):
        """切换页面并更新菜单状态"""
        self.stacked_widget.setCurrentIndex(index)
        # 更新菜单选中状态
        self.coord_action.setChecked(index == 0)
        self.ellipsoid_action.setChecked(index == 1)
        self.reserved_action.setChecked(index == 2)


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



############ 椭球计算 ############
    def init_ellipsoid_tab(self):
        """椭球计算功能页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 子标签容器
        sub_tabs = CalculationTabWidget()
        sub_tabs.addTab(self.create_curvature_ui(), "曲率半径")
        sub_tabs.addTab(self.create_arc_ui(), "子午线弧长")
        sub_tabs.addTab(self.create_convergence_ui(), "收敛角计算")
        
        layout.addWidget(sub_tabs)
        self.tab_widget.addTab(tab, "椭球计算")
        pass

    def create_curvature_ui(self):
        """曲率半径计算界面"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 参数输入
        param_group = QGroupBox("计算参数")
        param_layout = QFormLayout()
        
        self.ellipsoid_combo = QComboBox()
        self.ellipsoid_combo.addItems(ELLIPSOID_PARAMS.keys())
        
        self.start_b = QDoubleSpinBox()
        self.start_b.setRange(0, 90)
        self.end_b = QDoubleSpinBox()
        self.end_b.setRange(0, 90)
        self.step_b = QDoubleSpinBox()
        self.step_b.setValue(1.0)
        
        param_layout.addRow("椭球体:", self.ellipsoid_combo)
        param_layout.addRow("起始纬度(°):", self.start_b)
        param_layout.addRow("结束纬度(°):", self.end_b)
        param_layout.addRow("步长(°):", self.step_b)
        param_group.setLayout(param_layout)
        
        # 结果表格
        self.curvature_table = QTableWidget()
        self.curvature_table.setObjectName("curvature_table")  # 设置对象名称
        self.curvature_table.setColumnCount(5)
        self.curvature_table.setHorizontalHeaderLabels(["纬度", "M", "N", "R", "RA"])
        self.curvature_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # 操作按钮
        btn_calculate = QPushButton("开始计算", clicked=self.calculate_curvature)
        
        layout.addWidget(param_group)
        layout.addWidget(btn_calculate)
        layout.addWidget(self.curvature_table)
        return widget

    def calculate_curvature(self):
        """曲率半径计算"""
        try:
            ellipsoid = self.ellipsoid_combo.currentText()
            start = self.start_b.value()
            end = self.end_b.value()
            step = self.step_b.value()
            
            self.curvature_table.setRowCount(0)
            
            B = start
            while B <= end:
                result = EllipsoidCalculator.calculate_curvature(ellipsoid, B)
                row = self.curvature_table.rowCount()
                self.curvature_table.insertRow(row)
                self.curvature_table.setItem(row, 0, QTableWidgetItem(f"{B}°"))
                self.curvature_table.setItem(row, 1, QTableWidgetItem(f"{result['M']} m"))
                self.curvature_table.setItem(row, 2, QTableWidgetItem(f"{result['N']} m"))
                self.curvature_table.setItem(row, 3, QTableWidgetItem(f"{result['R']} m"))
                self.curvature_table.setItem(row, 4, QTableWidgetItem(f"{result['RA']} m"))
                B += step
                
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))    


    def create_arc_ui(self):
        """子午线弧长计算界面"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 参数输入
        param_group = QGroupBox("计算参数")
        param_layout = QFormLayout()
        
        self.arc_ellipsoid_combo = QComboBox()
        self.arc_ellipsoid_combo.addItems(ELLIPSOID_PARAMS.keys())
        
        self.arc_start_b = QDoubleSpinBox()
        self.arc_start_b.setRange(-90, 90)
        self.arc_start_b.setValue(30.0)
        
        self.arc_end_b = QDoubleSpinBox()
        self.arc_end_b.setRange(-90, 90)
        self.arc_end_b.setValue(36.0)
        
        param_layout.addRow("椭球体:", self.arc_ellipsoid_combo)
        param_layout.addRow("起始纬度(°):", self.arc_start_b)
        param_layout.addRow("结束纬度(°):", self.arc_end_b)
        param_group.setLayout(param_layout)
        
        # 结果展示
        self.arc_result_value = QLabel()
        self.arc_result_value.setObjectName("arc_result_value")  # 设置对象名称
        self.arc_result_value.setAlignment(Qt.AlignCenter)
        
        # 操作按钮
        btn_calculate = QPushButton("开始计算", clicked=self.calculate_arc_length)
        
        layout.addWidget(param_group)
        layout.addWidget(btn_calculate)
        layout.addWidget(self.arc_result_value)
        return widget

    def calculate_arc_length(self):
        """计算子午线弧长"""
        try:
            ellipsoid = self.arc_ellipsoid_combo.currentText()
            B1 = self.arc_start_b.value()
            B2 = self.arc_end_b.value()
            
            arc_length = EllipsoidCalculator.calculate_meridian_arc(ellipsoid, B1, B2)
            self.arc_result_value.setText(f"{arc_length:.3f} 米")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

    def create_convergence_ui(self):
        """平面子午线收敛角计算界面"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 参数输入
        param_group = QGroupBox("计算参数")
        param_layout = QFormLayout()
        
        self.gamma_ellipsoid_combo = QComboBox()
        self.gamma_ellipsoid_combo.addItems(ELLIPSOID_PARAMS.keys())
        
        self.gamma_b = QDoubleSpinBox()
        self.gamma_b.setRange(-90, 90)
        self.gamma_b.setValue(30.0)
        
        self.gamma_l = QDoubleSpinBox()
        self.gamma_l.setRange(-180, 180)
        self.gamma_l.setValue(1.5)
        
        param_layout.addRow("椭球体:", self.gamma_ellipsoid_combo)
        param_layout.addRow("纬度B(°):", self.gamma_b)
        param_layout.addRow("经差l(°):", self.gamma_l)
        param_group.setLayout(param_layout)
        
        # 结果表格
        self.gamma_table = QTableWidget()
        self.gamma_table.setObjectName("gamma_table")  # 设置对象名称
        self.gamma_table.setColumnCount(3)
        self.gamma_table.setHorizontalHeaderLabels(["纬度B", "经差l", "收敛角γ"])
        self.gamma_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # 操作按钮
        btn_calculate = QPushButton("开始计算", clicked=self.calculate_convergence)
        btn_clear = QPushButton("清空结果", clicked=lambda: self.gamma_table.setRowCount(0))
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(btn_calculate)
        button_layout.addWidget(btn_clear)
        
        layout.addWidget(param_group)
        layout.addLayout(button_layout)
        layout.addWidget(self.gamma_table)
        return widget

    def calculate_convergence(self):
        """计算子午线收敛角"""
        try:
            ellipsoid = self.gamma_ellipsoid_combo.currentText()
            B = self.gamma_b.value()
            l = self.gamma_l.value()
            
            gamma = EllipsoidCalculator.calculate_convergence(ellipsoid, B, l)
            
            row = self.gamma_table.rowCount()
            self.gamma_table.insertRow(row)
            self.gamma_table.setItem(row, 0, QTableWidgetItem(f"{B}°"))
            self.gamma_table.setItem(row, 1, QTableWidgetItem(f"{l}°"))
            self.gamma_table.setItem(row, 2, QTableWidgetItem(f"{gamma}°"))
            
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

############ GPS高程拟合 ############
    def create_gps_page(self):
        """GPS高程拟合页面"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 文件操作组
        file_group = QGroupBox("数据输入")
        file_layout = QHBoxLayout()
        self.gps_file_edit = QLineEdit()
        btn_browse = QPushButton("浏览", clicked=lambda: self.select_gps_file())
        file_layout.addWidget(QLabel("数据文件:"))
        file_layout.addWidget(self.gps_file_edit)
        file_layout.addWidget(btn_browse)
        file_group.setLayout(file_layout)
        
        # 参数选择组
        param_group = QGroupBox("拟合参数")
        param_layout = QHBoxLayout()
        self.gps_method_combo = QComboBox()
        self.gps_method_combo.addItems(["二次曲面拟合", "多项式平面", "四参数曲面"])
        param_layout.addWidget(QLabel("拟合方法:"))
        param_layout.addWidget(self.gps_method_combo)
        param_group.setLayout(param_layout)
        
        # 结果表格
        self.gps_table = QTableWidget()
        self.gps_table.setColumnCount(5)
        self.gps_table.setHorizontalHeaderLabels(["点号", "X", "Y", "ζ", "类型"])
        self.gps_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        self.btn_gps_calc = QPushButton("开始计算", clicked=self.calculate_gps)
        self.btn_gps_export = QPushButton("导出结果", clicked=self.export_gps)
        btn_layout.addWidget(self.btn_gps_calc)
        btn_layout.addWidget(self.btn_gps_export)
        
        layout.addWidget(file_group)
        layout.addWidget(param_group)
        layout.addWidget(self.gps_table)
        layout.addLayout(btn_layout)
        return tab
    
    def select_gps_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "选择数据文件", "", "文本文件 (*.txt)")
        if filename:
            self.gps_file_edit.setText(filename)
            self.load_gps_data(filename)

    def load_gps_data(self, filename):
        """加载并显示原始数据"""
        self.gps_table.setRowCount(0)
        try:
            with open(filename, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 3:  # 至少需要点号、X、Y三列
                        row = self.gps_table.rowCount()
                        self.gps_table.insertRow(row)
                        
                        # 点号
                        point_item = QTableWidgetItem(parts[0])
                        point_item.setForeground(QColor('#a0f0ff'))
                        self.gps_table.setItem(row, 0, point_item)
                        
                        # X坐标
                        x_item = QTableWidgetItem(parts[1])
                        x_item.setForeground(QColor('#a0f0ff'))
                        self.gps_table.setItem(row, 1, x_item)
                        
                        # Y坐标
                        y_item = QTableWidgetItem(parts[2])
                        y_item.setForeground(QColor('#a0f0ff'))
                        self.gps_table.setItem(row, 2, y_item)
                        
                        # 高程异常ζ（处理可能缺失的第四列）
                        if len(parts) >= 4 and parts[3].strip() != '':
                            z_value = parts[3]
                            type_flag = "已知"
                            z_color = QColor('#a0f0ff')
                        else:
                            z_value = "未知"
                            type_flag = "未知"
                            z_color = QColor('#ff6666')
                        
                        z_item = QTableWidgetItem(z_value)
                        z_item.setForeground(z_color)
                        self.gps_table.setItem(row, 3, z_item)
                        
                        # 类型
                        type_item = QTableWidgetItem(type_flag)
                        type_item.setForeground(QColor('#a0f0ff'))
                        self.gps_table.setItem(row, 4, type_item)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"文件读取失败: {str(e)}")

    def calculate_gps(self):
        try:
            # 提取已知点
            known_points = []
            for row in range(self.gps_table.rowCount()):
                if self.gps_table.item(row, 4).text() == "已知":
                    try:
                        x = float(self.gps_table.item(row, 1).text())
                        y = float(self.gps_table.item(row, 2).text())
                        z = float(self.gps_table.item(row, 3).text())
                        known_points.append((x, y, z))
                    except:
                        continue  # 跳过无效数据
            
            if not known_points:
                raise ValueError("至少需要1个已知点进行拟合")
            
            # 选择拟合方法
            method_map = {
                "二次曲面拟合": "quadratic",
                "多项式平面": "plane",
                "四参数曲面": "four_param"
            }
            method = method_map.get(self.gps_method_combo.currentText())
            if not method:
                raise ValueError("请选择有效的拟合方法")
            
            # 执行拟合
            predict_func = GPSFitter.fit(known_points, method)
            
            # 更新所有未知点
            updated_count = 0
            for row in range(self.gps_table.rowCount()):
                if self.gps_table.item(row, 4).text() == "未知":
                    try:
                        x = float(self.gps_table.item(row, 1).text())
                        y = float(self.gps_table.item(row, 2).text())
                    except ValueError:
                        continue  # 跳过无效坐标
                    
                    # 计算预测值
                    z_pred = predict_func(x, y)
                    
                    # 更新高程异常ζ
                    z_item = QTableWidgetItem(f"{z_pred:.4f}")
                    z_item.setForeground(QColor('#4d8fcc'))  # 计算结果颜色
                    self.gps_table.setItem(row, 3, z_item)
                    
                    # 更新类型
                    type_item = QTableWidgetItem("计算")
                    type_item.setForeground(QColor('#4d8fcc'))
                    self.gps_table.setItem(row, 4, type_item)
                    updated_count += 1
                    
            QMessageBox.information(self, "成功", 
                f"计算完成！共更新{updated_count}个未知点")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"计算失败: {str(e)}")

    def export_gps(self):
        try:
            filename, _ = QFileDialog.getSaveFileName(self, "保存结果", "", "CSV文件 (*.csv)")
            if filename:
                with open(filename, 'w', encoding='utf-8-sig') as f:
                    # 写表头
                    headers = ["点号", "X", "Y", "高程异常ζ", "类型"]
                    f.write(",".join(headers) + "\n")
                    
                    # 写数据
                    for row in range(self.gps_table.rowCount()):
                        row_data = []
                        for col in range(5):  # 5列数据
                            item = self.gps_table.item(row, col)
                            text = item.text() if item else ""
                            
                            # 格式化数值列
                            if col in (1, 2, 3):  # X/Y/ζ列
                                try:
                                    text = f"{float(text):.4f}"
                                except ValueError:
                                    pass
                            row_data.append(f'"{text}"')  # 添加引号防止格式错误
                        f.write(",".join(row_data) + "\n")
                QMessageBox.information(self, "成功", 
                    f"结果已保存到：\n{filename}\n包含{self.gps_table.rowCount()}条记录")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导出失败: {str(e)}")
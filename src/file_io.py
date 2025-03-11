# file_io.py
import os
import datetime

class FileHandler:
    def read_xyz_file(self, filename):
        data = []
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) != 4:
                    continue
                data.append({
                    'Point': parts[0].strip(),
                    'X': float(parts[1]),
                    'Y': float(parts[2]),
                    'Z': float(parts[3])
                })
        return data
    
    def format_blh_output(self, results):
        output = []
        for item in results:
            line = f"{item['Point']},{item['B']},{item['L']},{item['H']:.4f}"
            output.append(line)
        return '\n'.join(output)
    
    def format_site_output(self, results):
        output = []
        for item in results:
            line = f"{item['Point']},{item['N']*1000:.1f},{item['E']*1000:.1f},{item['U']*1000:.1f}"
            output.append(line)
        return '\n'.join(output)
    
    def save_blh_file(self, content):
        base_dir = os.path.join('result', 'Geodetic_Coordinates')
        os.makedirs(base_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(base_dir, f'GCC_{timestamp}.txt')
        with open(filename, 'w') as f:
            f.write(content)
        return filename
    
    def save_site_file(self, content):
        base_dir = os.path.join('result', 'Local_Cartesian_Coordinates')
        os.makedirs(base_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(base_dir, f'LCC_{timestamp}.txt')
        with open(filename, 'w') as f:
            f.write(content)
        return filename


    def read_gps_file(self, filename):
        """读取 GPS 数据文件"""
        data = []
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 3:  # 至少需要点号、X、Y三列
                    entry = {
                        'Point': parts[0].strip(),
                        'X': float(parts[1]),
                        'Y': float(parts[2]),
                        'Z': float(parts[3]) if len(parts) >= 4 and parts[3].strip() != '' else None,
                        'Type': "已知" if len(parts) >= 4 and parts[3].strip() != '' else "未知"
                    }
                    data.append(entry)
        return data
    
    def save_gps_file(self, gps_table_data):
        """保存 GPS 拟合结果到文件"""
        base_dir = os.path.join('result', 'GPS_Fitting_Result')
        os.makedirs(base_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(base_dir, f'GFR_{timestamp}.csv')
        
        with open(filename, 'w', encoding='utf-8-sig') as f:
            headers = ["点号", "X", "Y", "高程异常ζ", "类型"]
            f.write(",".join(headers) + "\n")
            for row in gps_table_data:
                row_data = []
                for col in row:  # 遍历每行数据
                    text = f'"{col}"' if isinstance(col, str) else f'"{col:.4f}"'
                    row_data.append(text)
                f.write(",".join(row_data) + "\n")
        return filename


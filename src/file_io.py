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
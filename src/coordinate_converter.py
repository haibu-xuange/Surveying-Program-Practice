# coordinate_converter.py

import math
import numpy as np

class CoordinateConverter:
    def __init__(self):
        self.ellipsoids = {
            "克拉索夫斯基": (6378245.0, 1/298.3),
            "WGS-84": (6378137.0, 1/298.257223563),
            "CGCS2000": (6378137.0, 1/298.257222101)
        }
    
    def xyz_to_blh(self, X, Y, Z, ellipsoid_name):
        a, f = self.ellipsoids[ellipsoid_name]
        b = a * (1 - f)
        e = math.sqrt(2*f - f**2)
        
        p = math.sqrt(X**2 + Y**2)
        theta = math.atan(Z * a / (p * b))
        
        L = math.atan2(Y, X)
        B = math.atan((Z + e**2 * b * math.sin(theta)**3) /
                     (p - e**2 * a * math.cos(theta)**3))
        
        N = a / math.sqrt(1 - e**2 * math.sin(B)**2)
        H = p / math.cos(B) - N
        
        # 迭代计算
        for _ in range(10):
            N = a / math.sqrt(1 - e**2 * math.sin(B)**2)
            H = p / math.cos(B) - N
            new_B = math.atan(Z / p * (1 - e**2 * N / (N + H))**(-1))
            if abs(new_B - B) < 1e-12:
                break
            B = new_B
        
        return self.rad_to_dms(B), self.rad_to_dms(L), H
    
    def xyz_to_site_coords(self, points, site_point):
        X0, Y0, Z0 = site_point['X'], site_point['Y'], site_point['Z']
        results = []
        
        for point in points:
            if point['Point'] == site_point['Point']:
                continue
            
            dX = point['X'] - X0
            dY = point['Y'] - Y0
            dZ = point['Z'] - Z0
            
            B, L, _ = self.xyz_to_blh(X0, Y0, Z0, "WGS-84")
            B = self.dms_to_rad(B)
            L = self.dms_to_rad(L)
            
            R = np.array([
                [-math.sin(L), math.cos(L), 0],
                [-math.sin(B)*math.cos(L), -math.sin(B)*math.sin(L), math.cos(B)],
                [math.cos(B)*math.cos(L), math.cos(B)*math.sin(L), math.sin(B)]
            ])
            
            enu = R @ np.array([dX, dY, dZ])
            results.append({
                'Point': point['Point'],
                'N': enu[0],
                'E': enu[1],
                'U': enu[2]
            })
        
        return results
    
    def rad_to_dms(self, radians):
        degrees = math.degrees(radians)
        d = int(degrees)
        m = int((degrees - d) * 60)
        s = ((degrees - d) * 60 - m) * 60
        return f"{d}° {m}' {s:.1f}\""
    
    def dms_to_rad(self, dms_str):
        parts = dms_str.replace('°', "'").replace('"', "'").split("'")
        d = float(parts[0])
        m = float(parts[1])
        s = float(parts[2])
        return math.radians(d + m/60 + s/3600)
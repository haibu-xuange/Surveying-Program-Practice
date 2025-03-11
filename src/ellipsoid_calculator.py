# ellipsoid_calculator.py
import math
from ellipsoid_params import ELLIPSOID_PARAMS

class EllipsoidCalculator:
    @staticmethod
    def get_ellipsoid(name):
        """获取指定椭球体参数"""
        params = ELLIPSOID_PARAMS.get(name)
        if not params:
            raise ValueError(f"未知椭球体: {name}")
        a = params['a']
        f = params['f']
        b = a * (1 - f)
        e2 = 2*f - f**2
        return a, b, f, e2

    @staticmethod
    def calculate_curvature(name, B_deg, A_deg=45):
        """计算曲率半径"""
        B = math.radians(B_deg)
        A = math.radians(A_deg)
        a, _, _, e2 = EllipsoidCalculator.get_ellipsoid(name)
        
        W = math.sqrt(1 - e2 * math.sin(B)**2)
        M = a*(1-e2) / (W**3)          # 子午圈曲率半径
        N = a / W                      # 卯酉圈曲率半径
        R = math.sqrt(M*N)             # 平均曲率半径
        RA = N / (1 + (N/M)*math.tan(A)**2)  # 任意方向曲率半径
        
        return {
            "M": round(M, 4),
            "N": round(N, 4),
            "R": round(R, 4),
            "RA": round(RA, 4)
        }

    @staticmethod
    def calculate_meridian_arc(name, B1_deg, B2_deg):
        """精确子午线弧长计算"""
        a, _, f, e2 = EllipsoidCalculator.get_ellipsoid(name)
        B1 = math.radians(B1_deg)
        B2 = math.radians(B2_deg)
        
        # 使用克拉克夫斯基展开式
        n = f / (2 - f)
        A0 = 1 + (n**2)/4 + (n**4)/64
        A2 = (3/2)*(n - (n**3)/8)
        A4 = (15/16)*(n**2 - (n**4)/4)
        A6 = (35/48)*n**3
        A8 = (315/512)*n**4
        
        def term(B):
            return a*(1-n)*(
                A0*(B - B1) 
                - A2*math.sin(2*B)/2 
                + A4*math.sin(4*B)/4 
                - A6*math.sin(6*B)/6 
                + A8*math.sin(8*B)/8
            )
        
        return term(B2) - term(B1)

    @staticmethod
    def calculate_convergence(name, B_deg, l_deg):
        """精确平面子午线收敛角计算"""
        B = math.radians(B_deg)
        l = math.radians(l_deg)
        a, _, f, e2 = EllipsoidCalculator.get_ellipsoid(name)
        
        t = math.tan(B)
        eta2 = e2 * math.cos(B)**2 / (1 - e2)
        
        gamma = l*math.sin(B) * (1 
               + (l**2/3)*(1 + 3*eta2 + 2*eta2**2)*math.sin(B)**2 
               + (l**4/15)*(2 - math.tan(B)**2))
        return round(math.degrees(gamma), 6)
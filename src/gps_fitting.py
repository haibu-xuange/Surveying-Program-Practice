# gps_fitting.py
import numpy as np
from scipy.optimize import curve_fit

class GPSFitter:
    @staticmethod
    def quadratic_model(coords, a, b, c, d, e, f):
        x, y = coords
        return a*x**2 + b*y**2 + c*x*y + d*x + e*y + f

    @staticmethod
    def plane_model(coords, a, b, c):
        x, y = coords
        return a*x + b*y + c

    @staticmethod
    def four_param_model(coords, a, b, c, d):
        x, y = coords
        return a*x + b*y + c*x*y + d

    @classmethod
    def fit(cls, known_points, method='quadratic'):
        """已知点格式：[(x1,y1,z1), ...]"""
        x = np.array([p[0] for p in known_points])
        y = np.array([p[1] for p in known_points])
        z = np.array([p[2] for p in known_points])
        
        if method == 'quadratic':
            popt, _ = curve_fit(cls.quadratic_model, (x,y), z, p0=[1]*6)
            func = lambda x,y: cls.quadratic_model((x,y), *popt)
        elif method == 'plane':
            popt, _ = curve_fit(cls.plane_model, (x,y), z, p0=[1]*3)
            func = lambda x,y: cls.plane_model((x,y), *popt)
        elif method == 'four_param':
            popt, _ = curve_fit(cls.four_param_model, (x,y), z, p0=[1]*4)
            func = lambda x,y: cls.four_param_model((x,y), *popt)
        return func
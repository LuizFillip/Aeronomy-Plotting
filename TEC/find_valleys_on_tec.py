import base as b 
import datetime as dt 
import plotting as pl 
import GEO as g
import scipy.interpolate
import pandas as pd 
from scipy.signal import find_peaks
import numpy as np 


dn = dt.datetime(2015, 12, 21, 0, 0)

def data_over_eq(dn):
    root = 'E:\\'
    
    dn_min = b.closest_datetime(
        b.tec_dates(dn, root = root), dn
        )
    
    infile = b.get_path(dn_min, root = root)
    lon, lat, tec = pl.load_tec(infile)
    
    lon_eq, lat_eq = g.load_equator(dn.year, values = True)
    
    tec_over_equator = []
    for i, lo in enumerate(lon):
        lat_alvo = lat_eq[i]
        f = scipy.interpolate.interp1d(
            lat, 
            tec[:, i], bounds_error = False
            )
        tec_val = f(lat_alvo)
        tec_over_equator.append((lo, lat_alvo, tec_val))
           
    df = pd.DataFrame(tec_over_equator)
    
    df.columns = ['lon', 'lat', 'tec']
    
    # df.tec = df.tec - df.tec.rolling(window = 10).mean()
    
    return df.lon, df.tec
def valleys_and_peaks(dn, desired_dx = 5 ):
    
 
    x, y = data_over_eq(dn)
    
    delta_x = np.mean(np.diff(x))
    
    min_dist = int(desired_dx / delta_x)
    
    valleys, _ = find_peaks(-y, distance=min_dist)
    
    # valleys = [i for i in valleys if y[i] < 0]
    
    return x[valleys], y[valleys]


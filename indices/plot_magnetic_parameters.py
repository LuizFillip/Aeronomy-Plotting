import base as b 
import core as c 
import numpy as np 


def plot_kp_by_range(ax, dn):
    
    ds = b.range_dates(c.low_omni(), dn, days = 4)
    ds = ds.resample('3H').mean() 
    
    ax.bar(
        ds.index, 
        ds['kp'] / 10, 
        width = 0.1,
        color = 'gray', 
        alpha = 0.5
        )
    ax.set(
        ylabel = 'Kp', 
        ylim = [0, 12], 
        yticks = np.arange(0, 12, 2)
        )
    
    ax.axhline(3, lw = 2, color = 'r')
    return None 

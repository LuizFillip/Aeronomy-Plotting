import numpy as np
import matplotlib.pyplot as plt
import settings as s
from common import load, sel_dates
import datetime as dt

def plot_indices_4():
    
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (15, 10),
        sharex = True,
        nrows = 3
        )
    
    plt.subplots_adjust(hspace = 0.1)
    

    start = dt.datetime(2013, 1, 1)
    end = dt.datetime(2015, 12, 31)
    
    dst_file = 'database/PlanetaryIndices/kyoto2000.txt'
    kp_file = "database/PlanetaryIndices/kp_postdam.txt"
    dst = sel_dates( 
        load(dst_file),
        start, end
        )
    
    ax[0].plot(dst)
    
    for h in [-50, -100]:
        ax[0].axhline(h, color = 'r', lw = 2)
        
    ax[0].set(
         ylim = [-200, 100],
         ylabel = "Dst (nT)"
         )
    
    
    kp = sel_dates(
        load(kp_file),
        start, end)
    
    x = kp.index
    y = kp["kp"].values
    
    ax[1].bar(x, y, width = 0.5, color = "black")
    
    ax[1].set(ylabel = 'Kp', 
              ylim = [0, 9], 
              yticks = np.arange(0, 9, 2)
              )
    
    for h in [3, 6]:
        ax[1].axhline(h, color = 'r', lw = 2)
    
    ax[2].plot(kp['F10.7a'])
    
    ax[2].set(ylabel = '$F_{10.7}$')
    
    ax[2].set(xlim = [start, end])
    s.axes_month_format(ax[2], 
                        month_locator = 4, 
                        pad = 60)
    
plot_indices_4()
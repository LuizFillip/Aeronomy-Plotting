import matplotlib.pyplot as plt
import base as s
import geophysical_indices as gd
import datetime as dt

    
s.config_labels()


def plot_dst(ax):
    
    infile = 'database/indices/kyoto2000.txt'
    dst = s.load(infile)
    
    dst = s.sel_dates(
        s.load(infile), 
        dt.datetime(2012, 12, 1), 
        dt.datetime(2023, 1, 13)
        )
    
    ax.plot(dst['dst'])
    
    ax.set(
        xlim = [dst.index[0], dst.index[-1]], 
        ylim = [-300, 70],
        ylabel = "Dst (nT)"
        )
    
    return dst



def plot_long_term():
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (14, 10), 
        nrows = 4, 
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    
    dialy = gd.GFZ()
    
    dialy = s.sel_dates(
        dialy, 
        dt.datetime(2012, 12, 1), 
        dt.datetime(2023, 1, 13)
        )
        
    
    ax[0].bar(dialy.index, dialy['kp_max'])
    ax[0].set(ylabel = 'Kp', 
              ylim = [0, 10], 
              yticks = np.arange(0, 9, 2))
    
    
    ax[0].axhline(4, lw = 2, color = 'r')
    
    plot_dst(ax[1])
    
    ax[2].plot(dialy['f107'])
    ax[2].plot(dialy['f107a'], 
               lw = 2, color='cornflowerblue')
    
    ax[2].set(ylabel = '$F_{10.7}$ (sfu)', 
              ylim = [50, 300])
    
    # df = s.load('pre_all_years_2.txt')

    # ax[3].scatter(df.index, df['vp'], s = 5)
    
    # avg = df['vp'].resample('1M').mean()
    # ax[3].plot(avg, color = 'r', lw = 2)
    ax[3].set(
        xlabel = 'years',
        ylabel = '$V_{zp}$ (m/s)', 
        ylim = [-10, 100], 
        xlim = [ dialy.index[0],  dialy.index[-1]])
    

import numpy as np

plot_long_term()
# df = s.load('pre_all_years.txt')

# df = df.replace(0, np.nan)

# df['doy'] = (df.index.day_of_year / 365) + df.index.year




# x = df['doy'].values
# y = df['vp'].values


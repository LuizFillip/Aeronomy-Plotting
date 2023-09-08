import matplotlib.pyplot as plt
import base as s
import datetime as dt
import numpy as np

    
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
        ylim = [-300, 100],
        yticks = np.arange(-300, 100, 100),
        ylabel = "Dst (nT)"
        )
    
    for limit in [-50, -100]:
        ax.axhline(limit, lw = 2, color = 'r')
    
    
    return dst



def plot_long_term():
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (14, 10), 
        nrows = 3, 
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    
    df = s.load('database/indices/indeces.txt')
    
    df = s.sel_dates(
        df, 
        dt.datetime(2012, 12, 1), 
        dt.datetime(2023, 1, 13)
        )
        
    
    ax[0].bar(df.index, df['kp_max'])
    ax[0].set(ylabel = 'Kp', 
              ylim = [0, 10], 
              yticks = np.arange(0, 10, 2)
              )
    
    
    ax[0].axhline(4, lw = 2, color = 'r')
    
    plot_dst(ax[1])
    
    ax[2].plot(df['f107'])
    ax[2].plot(df['f107a'], 
               lw = 2, 
               color = 'cornflowerblue'
               )
        
    ax[2].set(
        ylabel = '$F_{10.7}$ (sfu)', 
        ylim = [50, 300],
        yticks = np.arange(50, 350, 50),
        xlabel = 'years',
        xlim = [df.index[0], df.index[-1]]
        )
    
    for limit in [100, 150]:
        ax[2].axhline(limit, lw = 2, color = 'r')
        
        
    c = s.chars()
    s.config_labels(fontsize = 20)

    for i, ax in enumerate(ax.flat):
        
        ax.text(0.02, 0.85, f'({c[i]})', 
                transform = ax.transAxes)
    


plot_long_term()

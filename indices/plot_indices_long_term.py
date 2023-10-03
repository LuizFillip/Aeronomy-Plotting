import matplotlib.pyplot as plt
import base as s
import datetime as dt
import numpy as np
import PlasmaBubbles as pb 
    
s.config_labels()


def plot_dst(ax, dst):
    ax.plot(dst)
    
    ax.set(
        xlim = [dst.index[0], dst.index[-1]], 
        ylim = [-300, 100],
        yticks = np.arange(-300, 100, 100),
        ylabel = "Dst (nT)"
        )
    
    for limit in [-50, -100]:
        ax.axhline(limit, lw = 2, color = 'r')
    
    
    return dst

def plot_f107(ax, f107, f107a):
    
    ax.plot(f107)
    ax.plot(
        f107a, 
        lw = 3, 
        color = 'cornflowerblue'
        )
        
    ax.set(
        ylabel = '$F_{10.7}$ (sfu)', 
        ylim = [50, 250],
        yticks = np.arange(50, 250, 50)
        )

    for limit in [75, 110]:
        ax.axhline(
            limit, 
            lw = 2, 
            color = 'r'
            )
        
        
def plot_kp(ax, kp):
    
    ax.bar(kp.index, kp)
    
    ax.set(
        ylabel = 'Kp', 
        ylim = [0, 10], 
        yticks = np.arange(0, 10, 2)
        )
    
    ax.axhline(4, lw = 2, color = 'r')
     

def plot_long_term(s_year, e_year):
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (14, 10), 
        nrows = 3, 
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    df = s.load(pb.INDEX_PATH)
    
    df = s.sel_dates(
        df, 
        dt.datetime(s_year, 12, 1), 
        dt.datetime(e_year, 1, 13)
        )
        
    plot_kp(ax[0], df['kp'])
    plot_dst(ax[1], df['dst'])
    plot_f107(ax[2], df['f107'], df['f107a'])
  
    ax[2].set(
        xlabel = 'years',
        xlim = [df.index[0], df.index[-1]]
        )
        
    c = s.chars()
    s.config_labels(fontsize = 20)

    for i, ax in enumerate(ax.flat):
        
        ax.text(
            0.02, 0.85, f'({c[i]})', 
            transform = ax.transAxes
            )
        
    return fig
    


# f = plot_long_term(2012, 2023)

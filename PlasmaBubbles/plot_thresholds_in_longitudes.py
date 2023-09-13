import base as b 
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import PlasmaBubbles as pb 

b.config_labels()


args = dict(marker = 'o', 
            markersize = 1,
            linestyle = 'none', 
            color = 'k'
            )


def threshold(
        df, 
        percent = 0.8, 
        freq = 60
        ):
    
    dat = b.running(df.values, N = freq)
    
    vmax = dat.max() 
    vavg = dat.mean() 
        
    value = ((vmax + vavg) / 2 ) * percent
    
    if value < vavg:
        value = (vmax + vavg) * (1 + percent)
  
    return round(value, 2)
    
    
def plot_thresholds_example(
        ax, 
        df, 
        percent = 0.8, 
        freq = 60
        ):
    
    avg = b.running(df.values, N =  freq)
    ax.plot(df, **args)
    
    ax.plot(df.index, avg, lw = 2, 
            color = 'indigo')
    
    value = threshold(
        df, 
        freq = freq, 
        percent = percent
        )

    ax.axhline(
        value, 
        lw = 2, 
        color = 'r', 
        label = f'Threshold = {value} TECU/min'
        )
    
    ax.legend(loc = 'upper right')
    
    if value < 1:
        vmax = 1
    else:
        vmax = 5
        
    ax.set(ylim = [0, vmax],
           yticks = np.linspace(0, vmax, 5),
           ylabel = 'ROTI (TECU/min)', 
           )
    
    return ax
        




def plot_thresholds_in_longitudes(df, dn):
        
    df = b.sel_times(df, dn, hours = 11)
    
    fig, ax = plt.subplots(
        figsize = (12, 7), 
        dpi = 300,
        nrows = 2,
        sharex = True,
        sharey = True
        )
    
    plt.subplots_adjust(hspace = 0.1)
    c = b.chars()
    
    for i, col in enumerate(['-40', '-50']):
        
        plot_thresholds_example(ax[i], df[col])
        
        ax[i].text(0.01, 0.83, f'({c[i]}) Long = {col}°', 
                   transform = ax[i].transAxes
                   )
    
    b.format_time_axes(ax[1])
    
    ax[0].set(title = year)
    
    return fig
    
year = 2013
path = f'database/epbs/longs/{year}.txt'

df = b.load(path)
dn = dt.datetime(year, 6, 1, 20)

fig = plot_thresholds_in_longitudes(df, dn)


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

def plot_thresholds_example(
        ax, 
        df, 
        ):
    
    avg = b.running(df.values, N = 60)
    ax.plot(df, **args)
    
    ax.plot(df.index, avg, lw = 2, 
            color = 'indigo')
    
    dn = df.index[0]
    lon = int(df.name)
    
    value = pb.threshold(dn, lon)

    ax.axhline(
        value, 
        lw = 2, 
        color = 'r', 
        label = f'Threshold = {value} TECU/min'
        )
    
    ax.legend(loc = 'upper right')

    
    vmax = 4
        
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
        
        info =  f'({c[i]}) Long = {col}°'
        ax[i].text(
                0.01, 
                0.83,
                info, 
                transform = ax[i].transAxes
                 )
    
    b.format_time_axes(ax[1])
    
    year = df.index[0].year
    
    ax[0].set(title = year)
    
    return fig

def main():
    
    year = 2016
    
    path = f'database/epbs/longs/{year}.txt'
    
    df = b.load(path)
    dn = dt.datetime(year, 11, 1, 20)
    
    
    fig = plot_thresholds_in_longitudes(df, dn)

# main()
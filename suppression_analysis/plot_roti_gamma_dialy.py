import matplotlib.pyplot as plt
import base as b 
from indices import INDEX_HR
import os
import datetime as dt 
import core as c 

def plot_roti(ax, ds):
    
    ax.plot(ds['-50'])
    
    ax.set(ylim = [0, 3])
    
    b.format_days_axes(ax)
    
    ax.set(ylabel = 'ROTI')


def plot_index(ax, df, col = 'dst'):
    xmin, xmax = df.index[0], df.index[-1]
    
    ds = b.load(INDEX_HR)

    ds = b.sel_dates(ds, xmin, xmax)
    
    ax1 = ax.twinx()
    
    ax1.plot(ds[col], color = 'r')
    if col == 'bz':
        ylim = [-30, 30]
    elif col == 'dst':
        ylim = [-200, 20]
        
    ax1.set(
        ylim = ylim, 
        xlabel = 'days',
        ylabel = f'{col} (nT)', 
        xlim = [xmin, xmax]
            )

def plot_event(ax, event):

    ax.arrow(
        x= event, y=2, 
        dx=0, dy=-1, width=.08, 
        facecolor='red') 
    
    dn = event.strftime('%B, %Y')
    
    ax.text(0.01, 0.8, dn,
            transform = ax.transAxes)

def plot_roti_and_index(path, files):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = len(files), 
        figsize = (12, 10), 
        sharey = True
        )
    
    plt.subplots_adjust(hspace = 0.4)
    
    b.config_labels()
    
    
    
    delta = dt.timedelta(days = 1)
    
    # ax[nrows].set(xlabel = 'Days')
    
    for i, file in enumerate(files):
                
        df = b.load(path + file)
        
        plot_roti(ax[i], df)
        
        plot_index(ax[i], df)
        
        event = b.Filename2dn(file)

        plot_event(ax[i], event + delta)
    
    return fig 



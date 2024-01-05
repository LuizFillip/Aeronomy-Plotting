import matplotlib.pyplot as plt
import base as b 
from indices import INDEX_HR
import os
import datetime as dt 

def plot_roti(ax, ds):
    
    ax.plot(ds['-50'])
    
    dn = ds.index[0].strftime('%B, %Y')
    
    ax.text(0.01, 0.8, dn,
            transform = ax.transAxes)
    
    ax.set(ylim = [0, 5])
    
    b.format_days_axes(ax)
    
    # ax.set(ylabel = 'ROTI (TECU/min)')
    # ax1.set(ylabel = '$\\gamma_{RT} ~(s^{-1})$')


# df = c.concat_results('saa')



def plot_index(ax, df, col = 'dst'):
    xmin, xmax = df.index[0], df.index[-1]
    
    ds = b.load(INDEX_HR)

    ds = b.sel_dates(ds, xmin, xmax)
    
    ax1 = ax.twinx()
    
    ax1.plot(ds[col], color = 'r')
    if col == 'bz':
        ylim = [-30, 30]
    elif col == 'dst':
        ylim = [-150, 20]
        
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

def plot_roti_and_index(nrows = 2):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = nrows, 
        figsize = (10, 8), 
        sharey = True
        )
    
    plt.subplots_adjust(hspace = 0.4)
    
    b.config_labels()
    
    path = 'temp2/'
    files = os.listdir(path)[:nrows]
    
    delta = dt.timedelta(days = 1)
    
    for i, ax in enumerate(ax.flat):
        
        file = files[i]
        
        df = b.load(path + file)
        
        plot_roti(ax, df)
        
        plot_index(ax, df)
        
        event = b.Filename2dn(file)
        
        plot_event(ax, event + delta)
   

plot_roti_and_index(4)
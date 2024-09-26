import base as b 
import matplotlib.pyplot as plt 
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pandas as pd
import numpy as np 
import GEO as gg 

def plot_mean_std(
        ax, 
        vls, x = 0.1, y = 0.7, unit = 'HU'):
    
    mu = round(vls.mean(), 2)
    sigma = round(vls.std(), 2)
    mu = str(mu).replace('.', ',')
    sigma = str(sigma).replace('.', ',')
    
    
    
    info =  f'$\mu = $ {mu} {unit}\n$\sigma = $ {sigma} {unit}'
    
    ax.text(x, y, info, transform = ax.transAxes)
    
    return None 
    


def plot_histogram(
        ax, values, i, bins, xy = ()):
       
    args = dict(
        facecolor = 'lightgrey', 
        alpha = 1, 
        edgecolor = 'black',  
        color = 'gray'
        )

    divider = make_axes_locatable(ax)
    
    axHisty = divider.append_axes(
        "right", 2.5, 
        pad = 0.4, 
        sharey = ax)
    
    
    plt.setp( axHisty.get_yticklabels(), visible=False)
    
    bins = np.arange(min(bins), max(bins), 0.2)
    
    vls = values.ravel()
    
    counts, _, _ = axHisty.hist(
        vls,
        bins = bins, 
        orientation = 'horizontal',
        **args
        )
    
    step = 50
    axHisty.set(
        xlim = [0, max(counts) + step ],
        xticks = np.arange(10, max(counts) + step, step),
        xlabel = 'Frequência \n de ocorrência'
        )
    
    if i != 3:
        axHisty.set(
            xticklabels = [], 
            xlabel = ''
            )
    return axHisty 

def get_ticks(values, ds, step = 1):
    z, x, y = values.shape

    yticks = np.arange(20, 32 + step, step)
    start = ds.index[0].strftime('%Y-01-01')
    end = ds.index[-1].strftime('%Y-12-31')
    
    xticks = pd.date_range(start, end, periods = y)
    
    return xticks, yticks


def plot_terminator(
        ax, 
        sector, 
        midnight = True, 
        translate = True,
        label = False, 
        float_index = True,
        color = 'k'
        ):
    
    if translate:
        terminator_label = 'Solar terminator (300 km)'
        midnight_label = 'Local midnight'
    else:
        terminator_label = 'Terminadouro solar (300 km)'
        midnight_label = 'Meia-noite local'
    
    df = b.load('events_class2')
    
    df = df.loc[df['lon'] == sector]
    dn = df.index[0]
    dusk = gg.local_midnight(dn, sector, delta_day = None)
    
    dusk = round(b.dn2float(dusk))
    
    if float_index:
        df.index = (df.index.year + df.index.day_of_year / 365 )
        
    df['dusk'] = b.smooth2(df['dusk'], 4)
    
    ax.plot(df.index, df['dusk'], lw = 2, color = color)
   
    
    if label:
        ax.text(
            0.01, 0.05, 
            terminator_label, 
            color = color,
            transform = ax.transAxes
            )
    
    if midnight:
        
        if label:
            
            ax.text(
                dn, dusk + 0.5, 
                midnight_label, 
                color = 'w',
                transform = ax.transData
                )
        
        ax.axhline(dusk, lw = 2, color = color)
        
    
    ax.plot(
        df.index, 
        df['dusk'] + 2,
        linestyle = '--', 
        lw = 2, 
        color = color
        )
    
    return midnight, dusk
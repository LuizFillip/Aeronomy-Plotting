import core as c
import numpy as np
import base as b 
import matplotlib.pyplot as plt 

args = dict(capsize = 3, marker = 's')

def plot_cumullative(ax, ds, color):
     
     ax1 = ax.twinx()

     ax1.plot(ds['start'], 
               np.cumsum(ds['days']),
               lw = 2,
               color = color
               )
     
     ax1.set(ylim = [0, 1.2], 
             yticks = np.arange(0, 1.2, 0.25), 
             ylabel = 'Cumulated frequency')
     
     
def plot_histogram(
        ax, 
        ds, 
        index, 
        label = '', 
        parameter = 'gamma',
        width = 0.07,
        axis_label = False,
        translate = True
        ):
    
    if parameter == 'vp':
        xlabel = b.y_label('vp')
        width = 1.7
    elif parameter == 'gravity':
        xlabel = b.y_label('gamma')
        width = 0.015
    else:
        xlabel = b.y_label('gamma')
        width = 0.07
            
    days = int(ds['days'].sum())
        
    ax.bar(
        ds['start'] + (width * index),
        ds['days'], 
        width = width, 
        label = label
        )
     
    if axis_label:
        
        if translate:
            ylabel = 'Frequência de ocorrência'
        else:
            ylabel = 'Frequency of occurrence'

        ax.set(
            xlabel = xlabel, 
            ylabel = ylabel 
            )
    
    plt.xticks(rotation = 0)
    
    vmin, vmax, step = c.limits(parameter)
    
    ax.set(
        xlim = [vmin, vmax],
        xticks = np.arange(
            vmin, vmax + step, step*2
            )
        )
    
    
    return days

def plot_distribution(
        ax, 
        df, 
        parameter = 'gamma',
        label = '', 
        count = False,
        axis_label = False,
        translate = False,
        drop_ones = True,
        percent = True
        ):

    ds = c.probability_distribution(df, parameter)    
    
    if drop_ones:
        ds = ds.loc[~((ds['days'] == 1) & 
                      (ds['epbs'] == 1))].dropna()
        
    epbs = ds['epbs'].sum()
    
    if count:
        LABEL = f'{label} ({epbs} events)'
    else:
        LABEL = label
    
    if percent:
        factor = 100
        symbol = ' (\%)'
    else:
        factor = 1
        symbol = ''
        
    ax.errorbar(
        ds['start'], 
        ds['rate'] * factor, 
        xerr = ds['std'],
        yerr = ds['epb_error'] * factor,
        label = LABEL,
        **args
        )
    
    vmin, vmax, step = c.limits(parameter)
    
    if parameter == 'vp':
        xlabel = b.y_label('vp')
    else:
        xlabel = b.y_label('gamma')
    
    ax.set(
        xlim = [vmin, vmax],
        ylim = [-0.2* factor, 1.4* factor], 
        yticks = np.arange(0, 1.2* factor, 0.25* factor),
        xticks = np.arange(
            vmin, vmax + step, step*2
            ),
       
        )
    
    if translate:
        ylabel = 'Probalidade de ocorrência' + symbol
    else:
        ylabel = 'Occurrence probability' + symbol
        
    if axis_label:
        ax.set(
            xlabel = xlabel, 
            ylabel = ylabel
            )
    
    for bar in [0, 1* factor]:
        ax.axhline(
            bar, 
            linestyle = ":", 
            lw = 2, 
            color = "k"
            )
        
    return ds, epbs 




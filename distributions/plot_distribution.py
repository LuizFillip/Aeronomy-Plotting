import core as c
import numpy as np
import base as b 
import matplotlib.pyplot as plt 
from matplotlib.ticker import AutoMinorLocator

args = dict(capsize = 3, marker = 's')

def plot_cumullative(ax, ds, color):
     
     ax1 = ax.twinx()

     ax1.plot(ds['start'], 
               np.cumsum(ds['days']),
               lw = 2,
               color = color
               )
     
     ax1.set(
         ylim = [0, 1.2], 
        yticks = np.arange(0, 1.2, 0.25), 
        ylabel = 'Cumulated frequency'
        )
     
     
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
        width = 0.05
            
    days = int(ds['days'].sum())
    
    if index == 0:
        offset = (width / 2)
    else:
        offset = - (width / 2) * index
        
    ax.bar(
        ds['start'] + offset,
        ds['days'], 
        width = width, 
        label = label, 
        # fill = False
        )
     
    if axis_label:
        
        if translate:
            ylabel = 'Número de eventos'
        else:
            ylabel = 'Number of events'

        ax.set(
            xlabel = xlabel, 
            ylabel = ylabel 
            )
    
    plt.xticks(rotation = 0)

    return days

def plot_distribution(
        ax, 
        df, 
        parameter = 'gamma',
        label = '', 
        count = False,
        axis_label = False,
        translate = False,
        outliner = None,
        percent = True,
        limit = True,
        ylim = [0.2, 1.4]
        ):

    ds = c.probability_distribution(
        df, 
        parameter, 
        outliner = outliner,
        limit = limit
        )    
 
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
    
    ds['erro'] = (ds['epb_i'] + ds['epb_s'].abs()) / 2
    
    ax.errorbar(
        ds['start'], 
        ds['rate'] * factor, 
        xerr = ds['std'],
        yerr = ds['erro'] * factor,
        label = LABEL,
        **args
        )
    
    if limit:
        vmin, vmax, step = c.input_limits(parameter)
    else:
        vmin, vmax, step = c.compute_limits(df, parameter)
    
    vmin, vmax, step = 0, 1, 0.2
    
    if parameter == 'vp':
        xlabel = b.y_label('vp')
    else:
        xlabel = b.y_label('gamma')
    
    ax.set(
        xlim = [vmin - 0.1, vmax],
        ylim = [-ylim[0]* factor, ylim[-1]* factor], 
        yticks = np.arange(0, 1.2* factor, 0.25* factor),
        xticks = np.arange(vmin, vmax + step, step*2),
       
        )
    
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator(n=2))
    
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




import numpy as np
import matplotlib.pyplot as plt
import base as b
import core as c 
from plotting import plot_distribution



b.config_labels(fontsize = 25)

def plot_histogram(ax, dataset, index, name):
    
    width = 0.07

    ds = c.probability_distribuition(
        dataset,
        col
        )
    
    days = int(ds['days'].sum())
    
    offset = width * index
    
    ax.bar(
        ds['start'] + offset,
        ds['days'], 
        width = width, 
        label = name
        )
    
    ax.set(ylabel = 'Frequency of occurrence')
    
    ax.legend(loc = 'upper center', 
              ncol = 2)
    
    plt.xticks(rotation = 0)
    
    return days


def plot_distributions_solar_flux(
        df, 
        col = 'gamma',
        level = 86
        ):
    
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 2,
        sharex = True,
        figsize = (12, 12)
        )
    
    plt.subplots_adjust(hspace = 0.1)
        
    labels = [
        '$F_{10.7} < $' + f' {level}',
        '$F_{10.7} > $' + f' {level}'
        ]
    
  
    solar_dfs =  c.solar_levels(
        df, 
        level,
        flux_col = 'f107a'
        )
     
    total_epb = []
    total_day = []
    
    for i, ds in enumerate(solar_dfs):
        
        name = f'({i + 1}) {labels[i]}'
    
        epbs = plot_distribution(
            ax[1], 
            ds,
            col = col,
            label = name
            )
        
        days = plot_histogram(ax[0], ds, i, name)
        
        total_epb.append(epbs)
        total_day.append(days)
        
    
   
    
    print(total_epb, total_day)
  
    ax[1].legend(ncol = 2,  loc = 'upper center')
        
    
    return fig
 

df = c.concat_results('saa')

col = 'gamma'

fig = plot_distributions_solar_flux(
        df, 
        col,
        level = 86
        )



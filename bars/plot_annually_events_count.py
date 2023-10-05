# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 10:44:04 2023

@author: Luiz
"""

import PlasmaBubbles as pb 
import matplotlib.pyplot as plt
import base as b 


def plot_sunset_midnight_events(ds):
    
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 2,
        sharex = True,
        figsize = (12, 8)
        )

    period = ['sunset', 'midnight']
    
    plt.subplots_adjust(hspace = 0.1)
    ylims = [350, 40]
    for i, value in enumerate([1, 3]):
        
        df =  pb.month_occurrence(
            ds, value
            )
        
        total = int(df.values.sum())
    
        
        df.plot(
            kind = 'bar', 
            ax = ax[i], 
            legend = False
            )
        
        title = f'({b.chars()[i]}) Post {period[i]} '
        events = f'({total}  events)'
        
        plt.xticks(rotation = 0)
        
        ax[i].text(
            0.03, 0.85, 
            title + events, 
            transform = ax[i].transAxes
            )
        
        ax[i].set(
            ylabel = 'Nigths with EPB',
            xticklabels = b.number_to_months(), 
            ylim = [0, ylims[i]]
            )
        
   
    ax[0].legend(
        [f'{c}°' for c in ds.columns],
        ncol = 5, 
        title = 'Longitudinal sectors (2013-2022)',
        bbox_to_anchor = (.5, 1.4), 
        loc = "upper center", 
        columnspacing = 0.6
        )
    
    ax[1].set(xlabel = 'Months')

path = 'database/epbs/events_types.txt'

ds = b.load(path)

plot_sunset_midnight_events(ds)

# df =  pb.month_occurrence(ds, 3)


import matplotlib.pyplot as plt
import base as b
import core as c 
import plotting as pl 
 
b.config_labels()


def plot_single_year(
        ax, 
        ds, 
        label, 
        index = 0, 
        parameter = 'gamma'
        ):
    
    label = f'({index + 1}) {label}'
   
    data, epbs = pl.plot_distribution(
            ax[0], 
            ds,
            parameter,
            label,
            axis_label = True,
            drop_ones = True,
            translate = False
        )
    days = pl.plot_histogram(
            ax[1], 
            data, 
            index, 
            label, 
            parameter,
            axis_label = True,
            translate = False
        )
        
    
    ax[0].set(xlabel = '', ylim = [-10, 140])
    loc = 'upper center'
    ax[1].legend(ncols = 2, loc = loc)
    ax[0].legend(ncols = 2,  loc = loc)
    
    return epbs, days
    
                



def plot_compare_sites_in_year(
        year, parameter = 'gamma'
                               ):
    
    fig, ax = plt.subplots(
        figsize = (12, 8),
        dpi = 300,
        nrows = 2,
        sharex = True
        )
    
    
    plt.subplots_adjust(hspace = 0.05)
    
    
    df = c.concat_results('saa')
    
    df = df.loc[df.index.year == year]
    
    epbs, days = plot_single_year(
        ax, df, 'São Luís',
        index = 0, 
        parameter = parameter)
    
    
    ds = c.local_results(year)
    # ds = c.concat_results('jic')
    # ds = ds.loc[ds.index.year == year]
    
    epbs1, days1 = plot_single_year(
        ax, ds, 'Jicamarca', index = 1,
        parameter = parameter)
    
    
    
    
    ax[0].set(title = year)
    
    
    pl.plot_infos(ax[0], [epbs, epbs1])
    pl.plot_infos(ax[1], [days, days1])
    plt.show()
    return fig
# import numpy as np
for year in range(2013, 2021):
    
    fig = plot_compare_sites_in_year(year)
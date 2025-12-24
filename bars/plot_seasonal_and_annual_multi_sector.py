import matplotlib.pyplot as plt 
import base as b
import core as c
import GEO as gg 
import numpy as np 
# from matplotlib.ticker import AutoMinorLocator
# import plotting as pl 
# import datetime as dt 
import epbs as pb 

b.sci_format(fontsize = 25)

def plot_EPBs(ax, df, col = -50, translate = True):
    
    ds = c.seasonal_yearly_occurrence(
            df, 
            col = col
            )
    ds.index = ds.index.map(gg.year_fraction)

    ax.bar(
        ds.index + 0.1, 
        ds[col], 
        width = 0.08,
        edgecolor = 'black', 
        color = 'gray', 
        alpha = 0.7,
        linewidth = 2
        )
     
    if translate:
        ylabel = 'Número de casos'
    else:
        ylabel = 'Nights with EPB'
        
    # print(ds)
    ax.set(
        ylabel = ylabel, 
        # yticks = list(range(0, 12, 1)), 
        xticks = np.arange(2013, 2025, 1)
        )
        
    return ax.get_xlim()


def plot_seasonal_and_annual_multi_sector():
    
    fig, ax = plt.subplots(
         nrows = 3, 
         dpi = 300, 
         sharex = True,
         sharey = True,
         figsize = (14, 12)
         )
    
    plt.subplots_adjust(hspace = 0.1)
    infile = 'database/epbs/events_class2'
    ds = b.load(infile)
    
    
    df = pb.sel_typing(
             ds, 
             typing = 'midnight', 
             indexes = True, 
             year = 2023
             )
    
    sectors = np.arange(-70, -40, 10)[::-1]
    
    # df = df.loc[df['dst'] <= -30]
    
    for i, sector in enumerate(sectors):
        
        ax[i].text(
            0.02, 0.85, 
            f'Sector {i + 1}', 
            transform = ax[i].transAxes
            )
        plot_EPBs(ax[i], df, col = sector, translate = False)
    
    ax[-1].set(xlabel = 'Years')
    
    return fig


fig = plot_seasonal_and_annual_multi_sector()
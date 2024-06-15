import PlasmaBubbles as pb 
import base as b 
import matplotlib.pyplot as plt 
import plotting as pl  
from mpl_toolkits.axes_grid1 import make_axes_locatable




def plot_histogram(ax, df, parameter = 'start', n = 12):
    
    args = dict(
        facecolor='lightgrey', 
        alpha=1, 
        edgecolor = 'black',  
        color = 'gray'
        )


    
    divider = make_axes_locatable(ax)
    
    axHisty = divider.append_axes(
        "right", 2, pad = 0.2, sharey = ax)
    
    
    plt.setp( axHisty.get_yticklabels(),
              visible=False)

    df[parameter].plot(
        kind = 'hist', 
        ax = axHisty, 
        bins = b.bins(df, parameter, n), 
        orientation='horizontal',
        **args
        )
    
    # return None

def plot_hist_and_heatmap(ax, ds):
    
    
    df = pb.hourly_annual_distribution(
            ds, 
            normalize = True,
            step = 1, 
            percent = True
        )
    
    pl.plot_seasonal_hourly(
        ax,
        df, 
        cmap = 'jet',
        fontsize = 35, 
        translate = True,
        heatmap = True, 
        colorbar = False
        )
    
    
    # plot_histogram(ax, ds, parameter = 'start')
    
    args = dict(
        facecolor='lightgrey', 
        alpha=1, 
        edgecolor = 'black',  
        color = 'gray'
        )


    
    divider = make_axes_locatable(ax)
    
    axHisty = divider.append_axes(
        "right", 2, pad = 0.2, sharey = ax)
    
    
    plt.setp( axHisty.get_yticklabels(),
              visible=False)
    
    parameter = 'start'
    axHisty.hist(
        ds[parameter].values,
        bins = b.bins(ds, parameter, n = 10), 
        orientation='horizontal',
        **args
        )


    ax.set(ylim = [20, 32])


fig, ax = plt.subplots(
       ncols = 1,
       nrows = 4,
       dpi = 300, 
       sharex = True, 
       sharey = True,
       figsize = (16, 14)
       )


ds = b.load('events_class2')


ds = ds.loc[(ds['type'] == 'sunset')]


sectors = list(range(-80, -40, 10))[::-1]
for i, sector in enumerate(sectors):
    
    ds1 = ds.loc[ds['lon'] == sector]
    
    plot_hist_and_heatmap(ax[i], ds1)
    
    pl.plot_terminator(ax[i], sector)
    
    ax[i].set(title = f'Setor: {i + 1}')
    
   
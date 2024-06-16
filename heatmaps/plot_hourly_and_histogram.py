import PlasmaBubbles as pb 
import base as b 
import matplotlib.pyplot as plt 
import plotting as pl  
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pandas as pd
import numpy as np 



def plot_histogram(ax, values):
       
    args = dict(
        facecolor = 'lightgrey', 
        alpha = 1, 
        edgecolor = 'black',  
        color = 'gray'
        )

    divider = make_axes_locatable(ax)
    
    axHisty = divider.append_axes(
        "right", 2.5, pad = 0.2, sharey = ax)
    
    
    plt.setp( axHisty.get_yticklabels(),
              visible=False)
    
    bins = np.linspace(20, 32, 30)
    
    vls = values.ravel()
    
    axHisty.hist(
        vls,
        bins = bins, 
        orientation='horizontal',
        **args
        )


    axHisty.set(
   
        ylim = [20, 32], 
        xlim = [0, 1000]
        )
    
    b.plot_mean_std(axHisty, vls, )
    
    return axHisty 

def get_ticks(values, ds, step = 1):
    z, x, y = values.shape

    yticks = np.arange(20, 32 + step, step)
    start = ds.index[0].strftime('%Y-01-01')
    end = ds.index[-1].strftime('%Y-12-31')
    
    
    xticks = pd.date_range(start, end, periods = y)
    
    return xticks, yticks


def plot_hourly_and_histograms(
        ds,
        translate = False, 
        fontsize = 35
        ):
    
    

    fig, ax = plt.subplots(
           ncols = 1,
           nrows = 4,
           dpi = 300, 
           sharex = True, 
           sharey = True,
           figsize = (16, 14)
           )
    
    values = pb.annual_hourly_all_sectors(
            ds, 
            normalize = True,
            step = 1, 
            percent = True
        )
    
    
    xticks, yticks = get_ticks(values, ds, step = 1)
    sectors = list(range(-80, -40, 10))[::-1]
    
    
    for i, sector in enumerate(sectors):
        
        ds1 = ds.loc[ds['lon'] == sector]
            
        ax[i].imshow(
              values[i],
              aspect = 'auto', 
              extent = [xticks[0], xticks[-1], 
                        yticks[0], yticks[-1]],
              cmap = 'jet', 
              vmax = 100, 
              vmin = 0
              )
        
        plot_histogram(
            ax[i], ds1['start'].values )
        
        
        pl.plot_terminator(ax[i], sector, translate = False)
        
        l = b.chars()[i]
        s = f'({l}) Setor {i + 1}'
        
        ax[i].text(0., 1.05, s, transform = ax[i].transAxes)
        
    if translate:
        ylabel = 'Universal time'
        xlabel = 'Years'
        zlabel = 'Occurrence (\%)'
    else:
        xlabel = 'Anos'
        ylabel = 'Hora universal'
        zlabel = 'Ocorrência (\%)'
        
    b.fig_colorbar(
            fig,
            vmin = 0, 
            vmax = 100, 
            cmap = 'jet',
            fontsize = 25,
            step = 10,
            label = zlabel, 
            sets = [0.32, 0.98, 0.4, 0.02], 
            orientation = 'horizontal', 
            levels = 10
            )
    
    ax[-1].set(xlabel = xlabel)
    fig.text(
        0.045, 0.41, 
        ylabel, 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    return fig 

def main():
    ds = b.load('events_class2')
    
    type_in = 'sunset'
    ds = ds.loc[(ds['drift'] == 'fresh') & 
                (ds['type'] == type_in)]
    
    fig = plot_hourly_and_histograms(
        ds,
        translate = False )
         
    FigureName = f'seasonal_hourly_{type_in}'
    
    fig.savefig(
          b.LATEX(FigureName, 'climatology'),
          dpi = 400)

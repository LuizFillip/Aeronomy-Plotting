import matplotlib.pyplot as plt
import base as b 
import numpy as np
import plotting as pl 
import pandas as pd

b.config_labels(fontsize = 25)


lb = b.Labels().infos


names = ['Norte', 'Sul', 'Total']


def plot_height_prf(ax, ds, region = 'E'):
    
    if region == 'E':
        number = 7
    else:
        number = 2
        
    out = []
    for i, col in enumerate(['north', 'south']):
        name = names[i]
        df = ds.loc[ds['hem'] == col, region]
        out.append(df)
        ax.plot(
            b.smooth2(df, number), 
                df.index, 
                label = name)
        
        ax.set(xlabel = b.y_label("S"+ region))
        
    total = pd.concat(
        out, axis = 1
        ).dropna().sum(axis = 1)

    ax.plot(
        b.smooth2(total, number), 
        total.index, 
        label = 'Total')
    

    return total

def total_ratio(ax, region_E, region_F):

        
    ratio = region_F / (region_E + region_F) 
    
    ax.plot(b.smooth2(ratio, 2), 
            ratio.index, 
            lw = 1, label = 'Total', color = 'k')

    ax.set(
        xlabel = b.y_label('ratio'),
        xlim = [0.5, 1.2],
        )
    
    
    ax.axvline(1, linestyle = ':')


def plot_conductivities(df):
    
    fig, ax = plt.subplots(
        ncols = 3, 
        sharey= True,
        dpi = 300, 
        figsize = (14, 10))
    
    
    plt.subplots_adjust(wspace = 0.1, hspace = 0.1)
    
    region_E = plot_height_prf(ax[0], df, region = 'E')
    region_F = plot_height_prf(ax[1], df, region = 'F')
    total_ratio(ax[2], region_E, region_F)
    
    ax[0].set(ylabel = 'Altura de Apex (km)', 
              xticks = np.arange(0, 8, 1), 
              ylim = [100, 500]
              )
        
    ax[2].legend(ncol = 1,loc = "lower center")
    ax[1].legend(ncol = 1,loc = "lower right")
    b.plot_letters(ax, y = 1.03, x = 0.01)
    
    return fig
    
ds = pl.load_fluxtube()
fig = plot_conductivities(ds)


# FigureName = 'conductivities'

# fig.savefig(
#     b.LATEX(FigureName, folder = 'profiles'),
#     dpi = 400
#     )

import matplotlib.pyplot as plt
import base as b 
import numpy as np
import plotting as pl 
import pandas as pd

b.config_labels(fontsize = 35)


lb = b.labels


names = ['Norte', 'Sul', 'Total']

def total_ratio(ax, ds):
    
    for i, col in enumerate(['north', 'south']):
       
        region_E = ds.loc[ds['hem'] == col, 'E']
        region_F = ds.loc[ds['hem'] == col, 'F']
    
        ratio = region_F / (region_E + region_F) 
        
        ax.plot(b.smooth2(ratio, 2), ratio.index, lw = 1.5)

    ax.set(
        xlabel = b.y_label('ratio'),
        xlim = [0.5, 1.2],
        xticks = [0.6, 0.8, 1]
        )
    
    return None

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
        
        ax.plot(b.smooth2(df, number), 
                df.index, 
                label = name, lw = 1.5)
        
        ax.set(xlabel = b.y_label("S" + region))
        
    total = pd.concat(out, axis = 1).dropna().sum(axis = 1)
    
    
    ax.plot(
        b.smooth2(total, number), 
        total.index, 
        label = 'Total', lw = 1.5)
    

    return total




def plot_conductivities(df):
    
    fig, ax = plt.subplots(
        ncols = 3, 
        sharey = True,
        dpi = 300, 
        figsize = (16, 10)
        )
    
    
    plt.subplots_adjust(wspace = 0.1, hspace = 0.1)
    
    region_E = plot_height_prf(ax[0], df, region = 'E')
    region_F = plot_height_prf(ax[1], df, region = 'F')
    total_ratio(ax[2], df)
    
    ratio = region_F / (region_E + region_F) 
    
    ax[2].plot(b.smooth2(ratio, 2), ratio.index, lw = 1.5)
    
    ax[0].set(
        ylabel = 'Altura de Apex (km)', 
        xlim = [-2, 8],
        xticks = np.arange(0, 8, 2), 
        ylim = [100, 500]
        )

    ax[0].axvline(0, linestyle = '--')
        
    ax[1].legend(
        ncol = 3, 
        bbox_to_anchor = (.5, 1.15),
        loc = "upper center"
        )
    
    ax[2].axvline(1, linestyle = ':')
    
    ax[1].set(xticks = np.arange(0, 160, 40))
   
    b.plot_letters(ax, y = 0.92, x = 0.04, fontsize = 40)
    
    return fig

def main():
    ds = pl.load_fluxtube()
    fig = plot_conductivities(ds)
    
    
    FigureName = 'conductivities'
    
    fig.savefig(
        b.LATEX(FigureName, folder = 'profiles'),
        dpi = 400
        )

# main()
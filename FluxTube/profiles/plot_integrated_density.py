import plotting as pl 
import base as b
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


b.config_labels(fontsize = 25)

lb = b.Labels().infos


names = ['Norte', 'Sul', 'Total']
def plot_gradient(ax, ds):
    
    symbol = lb['K']['symbol']
    units = lb['K']['units']
    
    K = []
    for col in ['north', 'south']:
        
        df = ds.loc[ds['hem'] == col, 'K'] 
         
        K.append(df)
        ax.plot(b.smooth2(df * 1e5, 3), df.index)
    
    total = pd.concat(K, axis = 1).dropna().sum(axis = 1)

    ax.plot(total * 1e5, total.index)
    
    ax.set(
        xlim = [-1, 13], 
        xlabel = f'{symbol} ({units})', 
        xticks = np.arange(0, 14, 2)
        )
    
    ax.axvline(0, color = 'k', linestyle = '--')

    return 



def plot_density(ax, ds):
    
    out = []
    for i, col in enumerate(['north', 'south']):
        
        df = ds.loc[ds['hem'] == col, 'N']
        out.append(df)
        ax.plot(np.log10(df), df.index, 
                label = names[i])
    
    total = pd.concat(out, axis = 1).dropna().sum(axis = 1)

    ax.plot(np.log10(total), total.index, 
            label  = names[-1])
    
    ax.set(
        ylabel = 'Altura de Apex',
        xlim = [15, 20], 
        xticks = np.arange(15, 21, 1),
        xlabel = "log10($N_0$) ($cm^{-2}$)"
        )
    
    ax.legend(
        ncol = 3,
        bbox_to_anchor = (1., 1.15),
        loc = "upper center"
        )


def plot_ft_density_profiles(ds):
    '''
    This plot can be found in the subsection .. 
    in the chapter .. of the thesis
    
    '''
    fig, ax = plt.subplots(
        figsize = (10, 8),
        sharey = True,
        ncols = 2, 
        dpi = 300,
        
        )

    plt.subplots_adjust(wspace = 0.05)
    
    plot_density(ax[0], ds)
    
    plot_gradient(ax[1], ds)
    
    
    b.plot_letters(ax)
    return fig

ds = pl.load_fluxtube()

fig = plot_ft_density_profiles(ds)

FigureName = 'electron_density_and_gradient'

fig.savefig(
    b.LATEX(FigureName, folder = 'profiles'),
    dpi = 400
    )

import plotting as pl 
import base as b
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import models as m 


b.config_labels(fontsize = 25)

lb = b.labels


names = ['Norte', 'Sul', 'Total']

def plot_gradient(ax, ds):
    
    symbol = lb['K']['symbol']
    units = lb['K']['units']
    
    K = []
    for i, col in enumerate(['north', 'south']):
        
        df = ds.loc[ds['hem'] == col, 'K'] 
         
        K.append(df)
        ax.plot(b.smooth2(df * 1e5, 3), df.index, 
                label = names[i])
    
    total = pd.concat(K, axis = 1).dropna().sum(axis = 1)

    ax.plot(total * 1e5, total.index, label = 'Total')
    
    ax.set(
        xlim = [-5, 15], 
        xticks = np.arange(0, 18, 3),
        xlabel = f'{symbol} ({units})', 
        )
    
    ax.axvline(0, color = 'k', linestyle = '--')
    
    ax.legend(loc = 'upper right')
    return 


def plot_density(ax, ds):
    
    out = []
    for i, col in enumerate(['north', 'south']):
        
        df = ds.loc[ds['hem'] == col, 'N'] * 1e-18
        out.append(df)
        ax.plot(df, df.index, 
                label = names[i])
    
    total = pd.concat(out, axis = 1).dropna().sum(axis = 1)

    ax.plot(
        total, total.index, 
            label  = names[-1])
    
    ax.set(
        ylabel = 'Altura de Apex',
        xlim = [-1, 3], 
        xlabel = b.y_label('N', factor = 18)
        )
    
    return None


def plot_local_profiles(ax, ds):
    

    dn = ds['dn'].values[0]
   
    df = m.Equator_profiles(pd.to_datetime(dn))
    ax1 = ax[0].twiny()
    
    ax1.plot(
        df['ne'] * 1e-12,
        df.index, 
        lw = 2,
        color = 'k', 
        linestyle = '--', 
        label = 'Perfil local no equador'
        )
    
    ax1.set(xlabel = b.y_label('ne'), 
            xlim = [-1, 3])

    ax1.axvline(0, lw = 1, linestyle = ':')
    
    ax1 = ax[1].twiny()
    
    ax1.plot(
        df['L'] * 1e5,
        df.index, 
        color = 'k', 
        linestyle = '--', 
        lw = 2,
        label = 'Perfil local \nno equador')

    ax1.set(
        xlim = [-5, 15],
        xticks = np.arange(0, 18, 3),
        xlabel = b.y_label('L'),
        ylim = [150, 500]
        )
    
    ax1.axvline(0, lw = 1, linestyle = ':')
    ax1.legend(loc = 'center right')
    return 


def plot_ft_density_profiles(ds):
    '''
    This plot can be found in the subsection .. 
    in the chapter .. of the thesis
    
    '''
    fig, ax = plt.subplots(
        figsize = (12, 10),
        sharey = True,
        ncols = 2, 
        dpi = 300,
        
        )

    plt.subplots_adjust(wspace = 0.05)
    
    plot_local_profiles(ax, ds)
    
    plot_density(ax[0], ds)
    
    plot_gradient(ax[1], ds)
    
    b.plot_letters(ax, y = 0.92, x = 0.05)
    return fig

def main():
    ds = pl.load_fluxtube()
    
    fig = plot_ft_density_profiles(ds)
    
    FigureName = 'electron_density_and_gradient'
    
    fig.savefig(
        b.LATEX(FigureName, folder = 'profiles'),
        dpi = 400
        )
    


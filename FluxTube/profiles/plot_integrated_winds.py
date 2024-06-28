import base as b 
import matplotlib.pyplot as plt
import pandas as pd
import plotting as pl 
import numpy as np 

b.config_labels(fontsize = 30)

def plot_integrated_winds(ax, ds):
   
    names = ['Norte', 'Sul', 'Total']
    
    zon = []
    mer = []
    UL = []
    for i, col in enumerate(['north', 'south']):
        name = names[i]
        df = ds.loc[ds['hem'] == col].dropna()
        zon.append(df['zon_ef'])
        mer.append(df['mer_parl'])
        UL.append(df['mer_perp'])
        
        ax[0].plot(df['mer_parl'], df.index, label = name)
        ax[1].plot(df['zon_ef'], df.index, label = name)
        ax[i].axvline(0, linestyle = '--')
    
    
    ax[1].plot(total(zon), df.index, label = names[-1])
    
    ax[0].plot(total(mer), df.index, label = names[-1])
    
    ax[0].set(ylabel = 'Altura de Apex (km)', 
              xlim = [-50, 150],
              
              xticks = np.arange(0, 200, 50),
              xlabel = 'Velocidade meridional (m/s)')
    
    ax[1].set(ylim = [150, 500],
              xlim = [-50, 150],
              xticks = np.arange(0, 200, 50),
              xlabel = 'Velocidade zonal (m/s)')
    
    ax[2].plot(total(UL), df.index, lw = 2)
    ax[2].set(
        xlim = [-5, 5],
              xticks = np.arange(-4, 5, 1),
              xlabel = '$U_L^P$ (m/s)')
    ax[2].axvline(0, linestyle = '--')
    
     
    
def total(out):
    return pd.concat(out, axis = 1).sum(axis = 1)

def plot_local_winds(ax):
    
    infile = 'plotting/FluxTube/data/winds.txt'
    
    
    df = pd.read_csv(infile, index_col = 0)
   
    ax[0].plot(df['mer'], df.index, lw = 2, 
               linestyle = '--', color = 'k')
    
    ax[1].plot(df['zon'], df.index, lw = 2, 
               linestyle = '--', color = 'k',
               label = 'Perfil local no equador')
    

def plot_winds_profiles(ds):
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (18, 10),
        ncols = 3,
        sharey = True,
    
        )
    
    plt.subplots_adjust(
        wspace = 0.05
        )
    
    plot_local_winds(ax)
    

    plot_integrated_winds(ax, ds)
    
    ax[1].legend(
        ncol = 4, 
        bbox_to_anchor = (0.5, 1.13),
        loc = 'upper center',
        columnspacing = 0.5, 
        )
    
    b.plot_letters(ax, y = 0.95, x = 0.05)
    
    return fig

def main():
    ds = pl.load_fluxtube()
    
    fig = plot_winds_profiles(ds)
    
    FigureName = 'zonal_meridional_winds'
    
    fig.savefig(
        b.LATEX(FigureName, folder = 'profiles'),
        dpi = 400
        )


# main()
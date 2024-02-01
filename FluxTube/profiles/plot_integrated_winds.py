import base as b 
import matplotlib.pyplot as plt
import pandas as pd
import plotting as pl 

    

def plot_integrated_winds(ax, ds):
   
    names = ['Norte', 'Sul', 'Total']
    
    zon = []
    mer = []
    UL = []
    for i, col in enumerate(['north', 'south']):
        name = names[i]
        df = ds.loc[ds['hem'] == col].dropna()
        zon.append(df['zon'])
        mer.append(df['mer'])
        UL.append(df['mer_perp'])
        
        ax[0].plot(df['mer'], df.index, label = name)
        ax[1].plot(df['zon'], df.index, label = name)
        ax[i].axvline(0, linestyle = '--')
    
    
    ax[1].plot(total(zon), df.index, label = names[-1])
    
    ax[0].plot(total(mer), df.index, label = names[-1])
    
    ax[0].set(ylabel = 'Altura de Apex (km)', 
              xlim = [-100, 200],
              xlabel = 'Velocidade meridional (m/s)')
    
    ax[1].set(ylim = [100, 500],
              xlim = [-100, 200],
              xlabel = 'Velocidade zonal (m/s)')
    
    ax[2].plot(total(UL), df.index, lw = 2)
    ax[2].set(xlim = [-10, 10],
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
               label = 'Perfil local \nno equador')
    
    ax[1].legend(loc = 'lower right')

def plot_winds_profiles():
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (18, 10),
        ncols = 3,
        sharey = True,
    
        )
    
    plt.subplots_adjust(
        wspace = 0.15
        )
    
    plot_local_winds(ax)
    
    ds = pl.load_fluxtube()
    plot_integrated_winds(ax, ds)
    
    ax[0].legend(loc = 'lower right')
    
    b.plot_letters(ax, y = 1.03, x = 0.01)
    
    return fig


fig = plot_winds_profiles()


FigureName = 'zonal_meridional_winds'

fig.savefig(
    b.LATEX(FigureName, folder = 'profiles'),
    dpi = 400
    )

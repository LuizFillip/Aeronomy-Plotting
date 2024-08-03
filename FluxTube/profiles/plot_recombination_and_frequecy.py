import datetime as dt
import plotting as pl 
import base as b
import matplotlib.pyplot as plt
import pandas as pd
import models as m 
import aeronomy as ae

b.config_labels(fontsize = 30)

lb = b.labels


names = ['Norte', 'Sul', 'Total']

def plot_collision_freq(ax, ds):
    
    K = []
    for i, col in enumerate(['north', 'south']):
        
        df = ds.loc[ds['hem'] == col,  'nui'] 
         
        K.append(df)
        ax.plot(b.smooth2(df, 3), df.index, 
                lw = 1.5, label = names[i])
    
    total = pd.concat(K, axis = 1).dropna().sum(axis = 1)

    ax.plot(total, total.index, label = 'Total')
    
    ax.set(
        xscale ='log',  
        xlabel = b.y_label('nui_eff'),
        ylim = [100, 550]
        )
    
    ax.axvline(0, color = 'k', linestyle = '--')
    
    ax.legend(
        ncol = 4, 
        bbox_to_anchor = (0, 1.2),
        loc = "upper center",
        columnspacing = 0.5
        )
    
    return None


def plot_recombination(ax, ds):
    
    out = []
    for i, col in enumerate(['north', 'south']):
        
        df = ds.loc[ds['hem'] == col, 'R']
        out.append(df)
        
        ax.plot(df, df.index, lw = 1.5, label = names[i])
    
    total = pd.concat(out, axis = 1).dropna().sum(axis = 1)

    ax.plot(total, total.index, label  = names[-1])
    
    ax.set(
        xscale ='log', 
        ylabel = 'Altura de Apex',
        xlabel = b.y_label('R')
        )
    
    ax.axvline(0, color = 'k', linestyle = '--')
    
    return None 
  


def plot_local_profiles(ax, dn):
    
    df = m.altrange_models(
        **m.kwargs_from_meridian(dn, hmin = 100))
    df = ae.conductivity_parameters(df, other_conds = True)

    ax1 = ax[0]
    
    ax1.plot(
        df['R'],
        df.index, 
        lw = 2,
        color = 'k', 
        linestyle = '--', 
        label = 'Perfil local\nno equador')
    
    ax1.set(
        xscale ='log', 
        xlabel = b.y_label('nuR')
        )
 
    ax1.axvline(0, lw = 1, linestyle = ':')
    
    ax1 = ax[1]
    
    ax1.plot(
        df['nui'],
        df.index, 
        color = 'k', 
        linestyle = '--', 
        lw = 2,
        label = 'Perfil local \nno equador')

    ax1.set(
        xscale ='log', 
        xlabel = b.y_label('nui')
        )
    
    ax1.axvline(0, lw = 1, linestyle = ':')
    
    return 


def plot_ft_density_profiles(ds):
    '''
    This plot can be found in the subsection .. 
    in the chapter .. of the thesis
    
    '''
    fig, ax = plt.subplots(
        figsize = (14, 10),
        sharey = True,
        ncols = 2, 
        dpi = 300,
        
        )

    plt.subplots_adjust(wspace = 0.05)
    
    dn = dt.datetime(2013, 12, 24, 22)
    
    plot_local_profiles(ax, dn)
    
    plot_recombination(ax[0], ds)
    
    plot_collision_freq(ax[1], ds)
    
    b.plot_letters(ax, y = 0.92, x = 0.04, fontsize = 40)
    return fig

def main():
    ds = pl.load_fluxtube()
    
    fig = plot_ft_density_profiles(ds)
    
    FigureName = 'recombination_frequency'
    
    fig.savefig(
        b.LATEX(FigureName, folder = 'profiles'),
        dpi = 400
        )

# main()


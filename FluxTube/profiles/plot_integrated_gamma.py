import base as b 
import matplotlib.pyplot as plt
import pandas as pd
import plotting as pl 
import numpy as np
import models as m 
import aeronomy as ae

def gamma(ds):
    ds['vp'] = 30
    return ds['ratio'] * (ds['vp'] - (
        ds['ge'] / ds['nui'])) * ds['K'] - ds['R'] *0.1


def plot_integrated_parameters(ax, ds):
    

    names = ['Norte', 'Sul', 'Total']
    
    out = []
    
    for i, col in enumerate(['north', 'south']):
        name = names[i]
        df = gamma(ds.loc[ds['hem'] == col]).dropna()
        out.append(df)
           
        ax.plot(df * 1e3, df.index, label = name)
    
    ax.plot(pl.total(out)* 1e3, df.index, label = names[-1])
    ax.axvline(0, linestyle = '--')
    ax.axhline(300, linestyle = '--')
    
    
    
    ax.set(xlim = [-3, 3], 
           xticks = np.arange(-3, 4, 1),
           ylim = [150, 500], 
           ylabel = 'Altura de Apex (km)', 
           xlabel = b.y_label('gamma'))

def local_gamma(ds):
    
    dn = pd.to_datetime(ds['dn'].values[0])
    infile = 'plotting/FluxTube/data/winds.txt'
     
    wd = pd.read_csv(infile, index_col = 0)
    
    
    
    df = m.altrange_models(**m.kargs(dn, hmin = 80))
    df = ae.conductivity_parameters(df, other_conds = True)
    df['mer_perp'] = (wd['zon'] + wd['mer'])
    df['L'] = ae.scale_gradient(df['ne'], df.index)

    df['gamma'] =  df['L'] * (30  + (9.81 / df['nui']))  - df['R']
    return df

def plot_integrated_gamma():

    fig, ax = plt.subplots(
        ncols = 1,
        figsize = (8, 10), 
        dpi = 300
        )
    
    
    ds = pl.load_fluxtube()
    
    plot_integrated_parameters(ax, ds)
     
    
    df =  local_gamma(ds)
    
    
    
    ax.plot(df['gamma']* 1e3, df.index, lw = 2, 
            linestyle = '--', color = 'k',
            label = 'Perfil local\nno Equador')
    
    
    ax.legend()
    
    
    FigureName = 'gamma_local_integrated'
    fig.savefig(
        b.LATEX(FigureName, folder = 'profiles'),
        dpi = 400
        )
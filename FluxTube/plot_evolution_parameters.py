import pandas as pd
import matplotlib.pyplot as plt
import base as b 
import RayleighTaylor as rt
import datetime as dt 
import GEO as gg 


b.config_labels(fontsize = 25)

def pipe_data(dn):
    
    df = pd.read_csv('total_20131224', index_col=0)

    df = df.loc[df.index == 300]

    df.index = pd.to_datetime(df['dn'])

    df['vp'] = 46
    
    ds = rt.add_gammas(df)
    
    ds['gr'] = ds['ge'] / ds['nui']
    
    ds['K'] = ds['K'] *1e5
    ds['gamma'] = ds['gamma'] *1e3
    
  
    
    return b.sel_times(ds, dn, hours = 24)

def plot_growth_rate_parameters():
    fig, ax = plt.subplots(
        nrows = 5,
        figsize = (12, 14),
        sharex = True,
        dpi = 300
        )
    
    plt.subplots_adjust(hspace = 0.1)
    dn = dt.datetime(2013, 12, 24, 12)
    
    df = pipe_data(dn)
    
    lims = [[0.0, 1.2], 
            [0, 5], 
            [-30, 30], 
            [0, 40], 
            [0, 3]]

    cols = ['ratio', 'K', 
            'mer_perp',
            'gr', 'gamma']
    
    names = ['Norte', 'Sul']
    
    for i, col in enumerate(cols):
                
        out = []
        
        d = gg.dusk_time(
                dn,  
                lat = -2.53, 
                lon = -44.296, 
                twilight = 18,
                suni = 'dusk'
                )
        
        ax[i].axvline(d, lw = 1, linestyle = '--')
        d = gg.dusk_time(
                dn,  
                lat = -2.53, 
                lon = -44.296, 
                twilight = 18,
                suni = 'dawn'
                )
        
        ax[i].axvline(d, lw = 1, linestyle = '--')
        
        for j, hem in enumerate(['north', 'south']):
            
            ds = df.loc[df['hem'] == hem]
            
            out.append(ds[col])
            ax[i].plot(ds[col],
                       lw = 1.5,
                       label = names[j])
            
            ax[i].set(
                ylabel = b.y_label(col),
                ylim = lims[i])
        
        tl= pd.concat(out, axis = 1).sum(
            axis = 1)
        
        if col == 'ratio':
            tl = tl / 2
            
        ax[i].plot(
            tl, lw = 1.5, 
                   label = 'Total')
        
    b.format_time_axes(
        ax[-1], 
        translate = False, 
        hour_locator = 3
        )
    
    ax[0].legend( 
        ncol = 4, 
          bbox_to_anchor = (0.5, 1.5),
          loc = "upper center",
          columnspacing = 0.5
          )
    
    ax[0].axhline(1, linestyle = ':')
    ax[2].axhline(0, linestyle = ':')
    ax[-1].set(
        xlim = [df.index[0], df.index[-1]]
        )
    
    b.plot_letters(ax, y = 0.75, x = 0.02)

    return fig

     

def main():
    
    fig = plot_growth_rate_parameters()
    
    
    FigureName = 'gamma_parameters'
    
    fig.savefig(
        b.LATEX(FigureName, 
                folder = 'timeseries'),
        dpi = 400
        )
    

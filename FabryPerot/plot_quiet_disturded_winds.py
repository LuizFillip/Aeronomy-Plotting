import core as c 
import datetime as dt 
import matplotlib.pyplot as plt 
import FabryPerot as fp
import base as b
import pandas as pd 
import numpy as np 
import models 


PATH_FPI = 'database/FabryPerot/car/'

b.sci_format(fontsize = 25)

def average_of_directions(dn):
    
    wd = fp.FPI(PATH_FPI +  fp.fn(dn)).vnu
    
    out = []
    for coord in ['north', 'south']:
        
        ds = wd.loc[(wd["dir"] == coord)]
        ds = ds.loc[:, ['vnu', 'dvnu']].dropna()
        
        ds = fp.resample_new_index(ds, freq = '10min')
        ds.index = ds.index.to_series().apply(b.dn2float)
        ds.index = ds.index.where(ds.index >= 20, ds.index + 24)
        
        out.append(ds['vnu'])
        
    df = pd.concat(out, axis = 1).sort_index()
    df['avg'] = df.mean(axis = 1)
    df['std'] = df.std(axis = 1) / 2
    return df


def plot_quiettime_wind(ax, p = 'mer', translate = True):
    
    if translate:
        label = 'Quiet-time'
    else:
        label = 'Período calmo'
    dp = f'd{p}'
    
    qt =  c.quiettime_winds(coord = p)
    
    ax.plot(
        qt.index,
        qt[p], 
        color = 'purple', 
        lw = 2, 
        label = label, 
        marker = 's', 
        fillstyle = 'none'
        )
    
    
    ax.fill_between(
        qt.index, 
        qt[p] - qt[dp], 
        qt[p] + qt[dp], 
        color = "purple", 
        alpha = 0.3
        )
    
    return None 

def plot_TIEGCM(ax):
    
    dn = dt.datetime(2015, 12, 20, 20)
    
    df = models.tiecgm_data()
    
    ds = b.sel_times(df, dn, hours = 12) 
    
    ds.index = ds.index.to_series().apply(b.dn2float)
    ds.index = ds.index.where(ds.index >= 20, ds.index + 24)
        
    ax.plot(ds['mer'], color = 'blue', lw = 2, label = 'TIEGCM') 
    
    return None 

def plot_stormtime_wind(ax, dn, translate = True):
    
    if translate:
        label = 'Storm-time'
    else:
        label = 'Período perturbado'
        
        
    df = average_of_directions(dn)
    
    ax.plot(
        df.index,
        df['avg'], 
        color = 'k', 
        lw = 2, 
        label = label, 
        marker = 's', 
        fillstyle = 'none'
        )
    p = 'avg'
    dp = 'std'
    
    ax.fill_between(
        df.index, 
        df[p] - df[dp], 
        df[p] + df[dp], 
        color = "gray", 
        alpha = 0.3
        )
    return None 

def plot_quiet_disturbed_winds(dn, translate = True):
    
    if translate:
        ylabel = 'Meridional wind (m/s)'
        xlabel = 'Universal time'
        instr = 'FPI'
    else:
        ylabel = 'Vento Meridional (m/s)'
        xlabel = 'Hora Universal'
        instr = 'IFP'
        
    
    fig, ax = plt.subplots(
        figsize = (14, 5),
        dpi = 300,
       
        sharex = True,
        sharey = True
        )
    
    plot_stormtime_wind(ax, dn, translate)
    plot_quiettime_wind(ax, translate = translate)
    plot_TIEGCM(ax)
    
    ax.axhline(0, linestyle = '--')
   
    ylim = [-50, 180]
    step = 50
    yticks = np.arange(ylim[0], ylim[-1] + step, step)
    
    ax.set(
        ylabel = ylabel, 
        xlabel = xlabel,
        ylim = ylim, 
        yticks = yticks,
        xticks = np.arange(20, 33, 1),
        title = f'São João do Cariri - {instr}'
        )
    
    
    
    
    from matplotlib.ticker import FuncFormatter
    
    def wrap24(x, pos):
        return '0' + str(int(x-24)) if x >= 24 else int(x)

    ax.xaxis.set_major_formatter(FuncFormatter(wrap24))
    
    b.add_LT_axis(
        ax, 
        translate = translate
        )
    
    ax.legend(
        ncol = 3,
        loc = 'upper center'
        )
    
    return fig 



def main():
    date = dt.datetime(2015, 12, 20)
    
    fig = plot_quiet_disturbed_winds(date, translate=False)
    
    path_to_save = 'G:\\Meu Drive\\Papers\\Case study - 21 december 2015\\June-2024-latex-templates\\'
    
    FigureName = 'meridional_winds_pt'
    
    fig.savefig(
          path_to_save + FigureName,
          dpi = 400
          )

# main()


import core as c 
import datetime as dt 
import matplotlib.pyplot as plt 
import FabryPerot as fp
import base as b
import pandas as pd 
import numpy as np 

PATH_FPI = 'database/FabryPerot/car/'

b.sci_format(fontsize = 25)

def fn(dn):
    fmt = dn.strftime('%Y%m%d')
    return f'minime01_car_{fmt}.cedar.003.txt'


def plot_sky_component(ax, dn, direction, p = 'vnu'):

    wd = fp.FPI(PATH_FPI + fn(dn)).vnu
    
    ds = wd.loc[(wd["dir"] == direction)]
    ds = ds.loc[:, [p, f'd{p}']].dropna()
    ds.index = ds.index.to_series().apply(b.dn2float)
    ds.index = ds.index.where(ds.index >= 20, ds.index + 24)
    ds.loc[ds.index > 30, 'vnu'] = ds['vnu'] + ds['dvnu']
    # print(ds)
    ax.errorbar(
        ds.index, 
        ds[p], 
        yerr = ds[f'd{p}'], 
        capsize = 5,
        lw = 2,
        label = direction + ' (LOS)'
            )
    
    
    ax.axhline(0, linestyle = '--')
    
    return None 

def plot_total_variation(ax, ds, d = 'zon'):
    
    ds = component_avg(dn)
    
    for i, coord in enumerate(['zon', 'mer']):
        
        ax[i].errorbar(
            ds.index, 
            ds[coord], 
            yerr = ds[f'd{coord}'], 
            capsize = 5,
            lw = 2
                )
        
    
     
    return None 

def average_of_directions(dn):
    
    wd = fp.FPI(PATH_FPI + fn(dn)).vnu
    
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

def component_avg(dn):
    
    df = fp.FPI(PATH_FPI + fn(dn)).vnu
    
    df = fp.interpol_directions(
            df, 
            parameter = 'vnu',
            wind_threshold = 400
            )
    
    ds = pd.DataFrame()
    
    ds['mer'] = df[['north', 'south']].mean(axis = 1)
    ds['zon'] = df[['east', 'west']].mean(axis = 1)
    ds['dmer'] = df[['north', 'south']].std(axis = 1)
    ds['dzon'] = df[['east', 'west']].std(axis = 1)
    
    ds.index = ds.index.to_series().apply(b.dn2float)
    
    ds.index = ds.index.where(ds.index >= 20, ds.index + 24)
    return ds

def plot_quiettime_wind(ax, p = 'mer'):
    
    dp = f'd{p}'
    
    qt =  c.quiettime_winds(coord = p)
    
    
    ax.plot(
        qt.index,
        qt[p], 
        color = 'purple', 
        lw = 2, 
        label = 'Quiet-time', 
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
       

def plot_quiet_disturbed_winds(dn):
    
    # days = c.undisturbed_days(date, threshold = 18).index 
    
    fig, ax = plt.subplots(
        figsize = (14, 5),
        dpi = 300,
        # nrows = 2,
        sharex = True,
        sharey = True
        )
    
    df = average_of_directions(dn)
    
    ax.plot(
        df.index,
        df['avg'], 
        color = 'k', 
        lw = 2, 
        label = 'Storm-time', 
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
    
    plot_quiettime_wind(ax)
    
    ax.axhline(0, linestyle = '--')
   
    ylim = [-50, 150]
    step = 50
    yticks = np.arange(ylim[0], ylim[-1] + step, step)
    
    ax.set(
        ylabel = 'Meridional wind (m/s)', 
        xlabel = 'Universal time',
        ylim = ylim, 
        yticks = yticks,
        xticks = np.arange(20, 33, 1),
        title = 'São João do Cariri - FPI'
        )
    
    from matplotlib.ticker import FuncFormatter
    def wrap24(x, pos):
        return '0' + str(int(x-24)) if x >= 24 else int(x)

    ax.xaxis.set_major_formatter(FuncFormatter(wrap24))
    
    b.add_LT_axis(ax, offset_hours=-3, position = -0.25)
    ax.legend(
        ncol = 2,
        loc = 'upper center'
        )
    
    
    # b.plot_letters(ax, y = 0.85, x = 0.03)

    return fig 



def main():
    date = dt.datetime(2015, 12, 20)
    
    fig = plot_quiet_disturbed_winds(date)
    
    path_to_save = 'G:\\Meu Drive\\Papers\\Case study - 21 december 2015\\June-2024-latex-templates\\'
    
    FigureName = 'meridional_winds'
    
    fig.savefig(
          path_to_save + FigureName,
          dpi = 400
          )

main()



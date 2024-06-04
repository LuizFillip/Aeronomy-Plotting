import core as c 
import datetime as dt 
import matplotlib.pyplot as plt 
import FabryPerot as fp
import base as b
import pandas as pd 
import numpy as np 

PATH_FPI = 'database/FabryPerot/car/'


def fn(dn):
    fmt = dn.strftime('%Y%m%d')
    return f'minime01_car_{fmt}.cedar.003.txt'


def get_time_avg(data):
    
    
    out = []
    for df in data:
        try:
            out.append(
                fp.interpol_directions(
                    df, parameter = 'vnu'))
        except:
            continue
        
    df = pd.concat(out).sort_index()

    df['time'] = df.index.to_series().apply(b.dn2float)
    df['day'] = df.index.day
    df = df.loc[~df.index.duplicated()]

    out_dir = []
    for col in ['north', 'south', 'east', 'west']:
        
        ds2 = pd.pivot_table(
            df, 
            columns = 'day', 
            index = 'time', 
            values = col)
     
        out_dir.append(ds2.mean(axis = 1).to_frame(col))
        
    return pd.concat(out_dir, axis = 1)




def get_avg_coordinate(days,  winde = 300):
    
    data = []
    for dn in days:
        df = fp.FPI(PATH_FPI + fn(dn)).wind
        
        ds = df.loc[~(
            (df['vnu'] > winde) | 
            (df['vnu'] < -winde))
            ]
        data.append(ds)
    
    ds = get_time_avg(data)
    
    ds['mer'] = ds[['north', 'south']].mean(axis = 1)
    ds['zon'] = ds[['east', 'west']].mean(axis = 1)
    ds['dmer'] = ds[['north', 'south']].std(axis = 1)
    ds['dzon'] = ds[['east', 'west']].std(axis = 1)
    return ds

def plot_sky_component(ax, dn, direction, parameter = 'vnu'):

    wd = fp.FPI(PATH_FPI + fn(dn)).wind
    
    ds = wd.loc[(wd["dir"] == direction)]
    ds = ds.loc[:, [parameter, f'd{parameter}']].dropna()
    ds.index = ds.index.to_series().apply(b.dn2float)
    
    ax.errorbar(
        ds.index, 
        ds[parameter], 
        yerr = ds[f'd{parameter}'], 
        capsize = 5,
        lw = 2,
        label = direction + ' (LOS)'
            )
    
    ax.legend(ncol = 3, loc = 'upper center')
    
    ax.axhline(0, linestyle = '--')


def plot_quiet_variation(ax, ds, d = 'zon'):
    
    ax.errorbar(
         ds.index, 
         ds[d], 
         yerr = ds['d' + d], 
         capsize = 5,
         lw = 2,
         label = 'Quiet days',
         color = 'gray'
             )
     

def plot_quiet_disturbed_winds(date):
    
    days = c.undisturbed_days(date, threshold = 18).index 
    
    fig, ax = plt.subplots(
        figsize = (14, 10),
        dpi = 300,
        nrows = 2,
        sharex = True,
        sharey = True
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    ds = get_avg_coordinate(days)
    
    plot_quiet_variation(ax[0], ds, d = 'zon')
    plot_quiet_variation(ax[1], ds, d = 'mer')
    
    for coord in ['east', 'west']:
        plot_sky_component(ax[0], date, coord)
        
    for coord in ['north', 'south']:
        plot_sky_component(ax[1], date, coord)
    
   
    ylim = [-200, 400]
    step = 100
    yticks = np.arange(ylim[0], ylim[-1] + step, step)
    
    ax[1].set(
        ylabel = 'Meridional wind (m/s)', 
        xlabel = 'Universal time'
        )
    
    ax[0].set(
        ylabel = 'Zonal wind (m/s)', 
        ylim = ylim, 
        yticks = yticks,
        xticks = np.arange(20, 33, 1)
        )
    
    b.plot_letters(ax, y = 0.85, x = 0.03)

    return fig 


b.config_labels()

def main():
    date = dt.date(2015, 12, 20)
    
    fig = plot_quiet_disturbed_winds(date)
        
    FigureName = date.strftime('winds_%Y%m%d')
    
    fig.savefig(
          b.LATEX(FigureName, folder = 'paper2'),
          dpi = 400
          )

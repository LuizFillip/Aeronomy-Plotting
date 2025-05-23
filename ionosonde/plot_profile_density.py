import matplotlib.pyplot as plt 
import digisonde as dg 
import datetime as dt 
import base as b 


def plot_profiles_density_grads(df):
    fig, ax = plt.subplots(
            ncols =2,
            figsize = (10, 8),
            dpi = 300,
            sharey = True
            )
    plt.subplots_adjust(wspace = 0.1)
    
    for i in range(5, 10):
        dn = dt.datetime(year, month, i, 1, 0)
        
        ds = df.loc[(df.index == dn)]
        ax[0].plot(ds['ne'], ds['alt'], label = i)
        ax[1].plot(ds['L']*1e5, ds['alt'], label = i)
        ax[0].set(xlabel = 'Electron density (m3)', 
                  xlim = [0, 1.5e12])
        ax[1].set(xlabel = 'L (m2)', xlim = [-6, 6])
        ax[0].axhline(300)
        ax[1].axhline(300)
        
    plt.legend(title = 'days')
    ax[0].set(ylabel = 'Altura (km)')
    fig.suptitle(dn.strftime('%B-%Y (%Hh%M)'))
    
    return fig

year = 2015

import pandas as pd



fig, ax = plt.subplots(
        nrows = 3,
        figsize = (10, 12),
        dpi = 300,
        sharey = True, 
        sharex= True
        )
plt.subplots_adjust(wspace = 0.1)


sites = ['FZA0M', 'SAA0K', 'BVJ03']

for i, site in enumerate(sites):
    
    infile = f'digisonde/data/SAO/pro_profiles/{site}'

    df = dg.load_profilogram(infile)
 
    ds = pd.pivot_table(
        df, 
        index = 'alt', 
        columns = df.index, 
        values = 'ne') #.interpolate()
    
    ax[i].contourf(
        ds.columns, 
        ds.index, 
        ds.values, 30, cmap = 'jet'
        )
    ax[i].text(
        0.05, 0.8, site, 
               color = 'white',
               transform = ax[i].transAxes)
    delta = dt.timedelta(hours = 12)
    ax[i].set(
        xlim = [df.index[0] + delta, 
                      df.index[-1]])
    
b.format_time_axes(
    ax[-1], 
    hour_locator = 1, 
    pad = 70, 
    translate = True, 
    
    )
import matplotlib.pyplot as plt
import pandas as pd
import base as b
import numpy as np


def limits_wind(ds, cols):

    vmin = min([ds[col].min() for col in cols])
    vmax = max([ds[col].max() for col in cols])

    return vmin, vmax


def limits_iono(ds, cols):
    dic = {}
    
    for col in cols:
        dic[col] = (ds[col].min(), ds[col].max())
        
    return dic




def set_figure(
        ncols = 2, 
        nrows = 2, 
        figsize = (8, 10), 
        dpi = 300
        ):
    
    fig, ax = plt.subplots(
        dpi = dpi,
        figsize = figsize,
        ncols = ncols,
        nrows = nrows,
        sharex = True,
        sharey = True
        )
    
    plt.subplots_adjust(
        hspace = 0.2, 
        wspace = 0.1
        )
    
    return fig, ax
    
        
      
        


def plot(
        ax, ts, 
        parameter = "zon", 
        cmap = "rainbow"
        ):
    
    pt = pd.pivot_table(ts, values = parameter, 
                        columns = ts.index, 
                        index = "alt").interpolate().bfill()
    
    
    img = ax.contourf(
        pt.columns, pt.index, pt.values, 30, cmap = cmap
       )
    
    vls = pt.values
    ticks = np.linspace(np.min(vls), np.max(vls), 5)
    
    
    
    if parameter == "ratio":
        label = lbs["symbol"] 
    else:
        label = f"{lbs['symbol']} ({lbs['units']})"
    
    b.colorbar_setting(
            img, ax, ticks, 
            label = label)
    
    
parameter = 'sigma'
lbs  = b.Labels().infos[parameter]

ax.set(title = lbs["name"].replace("\n", " "))

df = pd.read_csv('20131224sep.txt', index_col = 0)

dn = '2013-12-24 20:00:00'

ds = df.loc[df['dn'] == dn]

ds = ds.loc[ds['hem'] == 'north']

plt.plot(ds['F'], ds.index)
plt.plot(ds['E'], ds.index)
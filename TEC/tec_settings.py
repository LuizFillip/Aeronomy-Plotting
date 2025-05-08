import pandas as pd
import numpy as np
import datetime as dt 
import base as b 
import matplotlib.pyplot as plt 

def load_tec(infile, values = True):

    df = pd.read_csv(
        infile, 
        delimiter = ';', 
        header = None
        ).replace(-1, np.nan)
    
    xmax, ymax = df.values.shape
   
    df.columns = np.arange(0, ymax)*0.5 - 90
    df.index = np.arange(0, xmax)*0.5 - 60
    
    if values:
        return df.columns, df.index, df.values
    else:
        return df

# sel = df.loc[
#      ((df.index > -10) & (df.index < 10)), 
#      (df.columns > -50) & (df.columns < -40)
#        ]

# return np.nanmean(sel.values)

def load_from_dn(dn, root = 'E:\\'):
    
    path = b.get_path(dn, root = root)
        
    return load_tec(path, values = False) 


day = 20

lon = -50

def make_keo(day, lon):
    
    times = pd.date_range(
         f'2015-12-{day} 21:00',
         f'2015-12-{day + 1} 08:00', 
         freq = '10min'
         )

    out = []
    for dn in times:
    
    
        ds = load_from_dn(dn, root = 'E:\\')
        
        out.append(ds.loc[:, ds.columns == lon])
        
    df = pd.concat(out, axis = 1)
    
    df.columns = times
    
    return df 

def plot_keogram_tec():
    
    fig, ax = plt.subplots(
        figsize = (16, 12), 
        nrows = 3
        )
    
    for i, day in enumerate([19, 20, 21]):
        
        
        df = make_keo(day, lon)
        
        ax[i].contourf(
            df.columns, 
            df.index, 
            df.values, 
            20, 
            cmap = 'jet'
            ) 
        
        ax[i].set(
            ylabel = 'Latitude (°)',
            ylim = [-40, 0], 
                  )
        ax[i].text(
            0.01, 0.85, 
            f'{day} - {day + 1} December 2015', 
            transform = ax[i].transAxes, 
            fontsize = 30
            )
        b.axes_hour_format(
                ax[i], 
                hour_locator = 1)
        
        if i == 2:
            ax[i].set(xlabel = 'Universal time')
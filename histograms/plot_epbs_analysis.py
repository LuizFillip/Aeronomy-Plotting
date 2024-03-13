import matplotlib.pyplot as plt 
import core as c 
import numpy as np
import base as b

path = 'events_2013_2023'


args = dict(facecolor='lightgrey', 
             alpha=1, 
             edgecolor = 'black',  
             color = 'gray')


fig, ax = plt.subplots(
    ncols = 4,
    nrows = 3,
    figsize = (18, 12),
    dpi = 300,
    sharey = 'row'
    )

ds = b.load(path)

plt.subplots_adjust(wspace = 0.05, hspace = 0.5)

for col, lon in enumerate(ds.lon.unique()):
    
    df = ds.loc[ds['lon'] == lon]
    
    df['start'].plot(
        kind = 'hist', 
        ax = ax[0, col], 
        bins = np.arange(20, 28, 0.5), 
        **args  
        )
    
    df['shift'].plot(
        kind = 'hist', 
        ax = ax[1, col], 
        bins =  np.arange(-1, 6, 0.4), 
        **args 
        )
    
    df['duration'].plot(
        kind = 'hist', 
        ax = ax[2, col], 
        bins = np.arange(0, 10, 0.5), 
        **args  
        )
    
    ax[0, col].set(title = f'{lon}°')
    
    fig.text()
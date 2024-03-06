import pandas as pd 
import matplotlib.pyplot as plt 
import base as b 
import os 

files = ['202110', '202203', '202209']

def set_data(file, values = 'zon'):
    infile = 'database/HWM/winds_bjl_' + file
    
    df = b.load(infile)
    
    df['day'] = df.index.day 
    df['time'] = b.dn2float(df.index, sum_from = None)
    
    return pd.pivot_table(
        df, 
        columns = 'day', 
        index = 'time', 
        values = values
        )

b.config_labels()

fig, ax = plt.subplots(
    nrows = 3,
    dpi= 300,
    sharex = True, sharey=True, 
    figsize = (10, 8)
    )


for i, file in enumerate(files):
    ds = set_data(file)

    ax[i].plot(ds, color = 'gray', alpha = 0.4)
    ax[i].plot(ds.mean(axis = 1), lw = 3, 
               color = 'k', label = 'Zonal')
    
    ax[i].set(ylim = [-150, 150])
    
    ds = set_data(file, values = 'mer')

    ax[i].plot(ds, color = 'gray', alpha = 0.4)
    ax[i].plot(ds.mean(axis = 1), lw = 3,
               color = 'b', label = 'Meridional')
    
    ax[i].axhline(0, linestyle = '--')
    
ax[0].legend(ncol = 2, loc = 'upper center')
ax[2].set(xlabel = 'Universal time')
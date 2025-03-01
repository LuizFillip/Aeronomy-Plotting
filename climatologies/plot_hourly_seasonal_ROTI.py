import numpy as np 
import matplotlib.pyplot as plt 
import base as b 
import pandas as pd 
import datetime as dt

b.config_labels()

def concat_years():
    out = []
    for year in range(2013, 2023):
        
        infile = f'database/epbs/longs/{year}'
        
        df = b.load(infile)
        
        df.loc[df.between_time('23:58', '00:02').index, :] = np.nan
        
        df = df.interpolate()
        df['time'] = b.time2float(df.index)
        
        df['date'] = df.index.date
        
        out.append(df)
    
    
    ds = pd.pivot_table(
        pd.concat(out), 
        columns = 'date', 
        index = 'time', 
        values = '-50'
        )
    return ds 
infile = 'database/epbs/maximus'

df = b.load(infile)

df['time'] = b.time2float(df.index)

    
df['date'] = df.index.date


df = df.resample('30min').mean()

ds = pd.pivot_table(
    df, 
    columns = 'date', 
    index = 'time', 
    values = '-50'
    )

ds = ds.replace(np.nan, 0)
ds = ds.interpolate(method = 'quadratic')

fig, ax = plt.subplots(
    figsize = (16, 8), 
    dpi = 300)

img = ax.contourf(
    ds.columns, 
    ds.index, 
    ds.values,
    levels = np.arange(0, 2.2, 0.2)
    )


plt.colorbar(img)


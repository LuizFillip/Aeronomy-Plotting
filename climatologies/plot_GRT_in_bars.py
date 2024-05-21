# -*- coding: utf-8 -*-
import pandas as pd 
import base as b 
import datetime as dt 
import matplotlib.pyplot as plt 

PATH_GAMMA = 'database/gamma/p1_saa.txt'

df = b.load(PATH_GAMMA)

df = df.loc[(df.index.time == dt.time(22, 0)) & 
            (df.index.year < 2023)]

df['gr'] = df['ge'] / df['nui']
df['gamma'] = df['gamma'] *1e3
df['K'] = df['K'] * 1e5 

ds = df.resample('1Y').mean()

ds.index = ds.index.year 

fig, ax = plt.subplots(
    sharex = True,
    dpi = 300, 
    nrows = 6, 
    figsize = (12, 18), 
    )


cols = ['ratio', 'vp', 'mer_perp', 'K', 
        'gr', 'gamma']

limits = [
    
    ]
for i, col in enumerate(cols):
    
    ax[i].bar(ds.index, ds[col], width = 5)
    
    
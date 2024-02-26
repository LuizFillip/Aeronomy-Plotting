# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 15:10:23 2024

@author: Luiz
"""

import matplotlib.pyplot as plt 
import digisonde as dg 
import datetime as dt 
import base as b 

year = 2015

infile = f'digisonde/data/jic/profiles/{year}'

df = dg.load_profilogram(infile)
df['L'] = b.smooth(df['L'], 20)
time = dt.time(1, 0)

for i in range(6, 10):
    dn = dt.datetime(year, 1, i, 1, 0)
    
    ds = df.loc[(df.index == dn)]
    
    plt.plot(ds['L'], ds['alt'], label = i)
    
plt.legend()
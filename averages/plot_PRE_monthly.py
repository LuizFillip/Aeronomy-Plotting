import numpy as np 
import base as b 
import core as c 
import pandas as pd 
import matplotlib.pyplot as plt 


df = c.load_results()

df = df.loc[:, ['vp']]
df = df.resample('1M').mean()
df['year'] = df.index.year
df['month'] = df.index.month

ds = pd.pivot_table(df, values = 'vp', columns = 'year', index = 'month')



fig, ax = plt.subplots(
    dpi = 300, 
    figsize = (14, 6)
    )

ax.errorbar(
    ds.index, 
    ds.mean(axis = 1),
    yerr = ds.std(axis = 1),
    marker = 's',
    capsize = 5,
    lw = 2, 
    
    )

ax.set(
       title = 'Monthly average over São Luís',
       xlabel = 'Months', 
       ylabel = 'Vertical drift (m/s)',
       xticks = np.arange(1, 13, 1),
       xticklabels = b.month_names(
           sort = True, language = 'en'),
       
       )
plt.show()
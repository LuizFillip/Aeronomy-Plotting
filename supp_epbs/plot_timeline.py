import plotting as pl 
import matplotlib.pyplot as plt
import numpy as np
import core as c 
import base as b 

b.sci_format(fontsize = 25)


def setdata():
    df = b.load('core/src/geomag/data/stormsphase')
    
    df = c.geomagnetic_analysis(df)
    
    df['year'] = df.index.year
    
    ds = df.groupby(
        ['category','year']
        ).size().unstack(fill_value = 0)
    
    return ds.T[['intense', 'moderate', 'weak', 'quiet']]

def plot_bars_stacked(ax):
    
    ds = setdata()

    colors = {
        'intense': '#8B0000',   # vermelho escuro
        'moderate': '#FF4500',  # laranja forte
        'weak': '#FFD700',      # dourado
        'quiet': '#32CD32'      # verde
    }
    
    ds.plot(
            kind = 'bar',
            stacked=True,
            ax = ax,
            color = [colors[c] for c in ds.columns]
            )
    
    
    plt.xticks(rotation = 0)
    
    pl.legend_for_sym_h(ax, quiet = True)
    
    
    
    
fig, ax = plt.subplots(
    nrows = 2,
    figsize = (12, 10))



# fig.align_ylabels()
import pandas as pd 

df = b.load('maximums_roti')
df['date'] = pd.to_datetime(df['date'])
df['date'] = df.index.year + df.index.month / 12 + df.index.day / 31
ds = df.pivot(
    index = 'time', 
         columns = 'date', 
         values = '-50') 


img = ax[0].contourf(
    ds.columns, 
    ds.index, 
    ds.values,
    
    levels = np.arange(0, 2.2, 0.2), 
    cmap = 'rainbow'
    )


ds = b.load('core/src/geomag/data/stormsphase')

ax[0].scatter(ds.index, np.ones(len(ds)) * 22, color = 'white')

plot_bars_stacked(ax[1])

# plt.colorbar(img)
import plotting as pl 
import matplotlib.pyplot as plt
import numpy as np
import core as c 
import base as b 

b.sci_format(fontsize = 25)


df = b.load('core/src/geomag/data/stormsphase')


df = c.geomagnetic_analysis(df)

df['year'] = df.index.year

ds = df.groupby(
    ['category','year']
    ).size().unstack(fill_value = 0)

ds = ds.T[['intense', 'moderate', 'weak', 'quiet']]
fig, ax = plt.subplots(figsize = (12, 6))

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
color=[colors[c] for c in ds.columns])


plt.xticks(rotation = 0)

pl.legend_for_sym_h(ax, quiet = True)
fig.align_ylabels()
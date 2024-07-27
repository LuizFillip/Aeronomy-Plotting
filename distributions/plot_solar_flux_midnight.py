import matplotlib.pyplot as plt
import base as b
import core as c 
import plotting as pl 
import numpy as np  

b.config_labels(fontsize = 25, blue = True)

legend_args = dict(
    ncol = 3, 
    loc = 'upper center', 
    labelcolor = 'linecolor',
    fontsize = 20,
    columnspacing = 0.2,
    )


df = c.load_results(typing = 'midnight')

 
fig, ax = plt.subplots(
    dpi = 300, 
    nrows = 2,
    sharex = True,
    figsize = (12, 10)
    )

plt.subplots_adjust(hspace = 0.05)
parameter = 'gamma2'
translate = True

ds, epbs = pl.plot_distribution(
        ax[0], 
        df,
        parameter = parameter,
        label = '',
        axis_label = True,
        outliner = 10, 
        translate = translate ,
        limit = False
    )

ax[1].bar(
    ds['start'],
    ds['days'], 
    width = 0.02
    )

# df.loc[df['epb'] == 1]['gamma2'].plot()
ax[0].set(xlabel = '', 
          ylim = [-10, 110])
ax[1].set(
    ylabel = 'Número de eventos',
    xlim = [0, 0.8], 
          xlabel = '$\gamma_{RT} (10^{-3} s^{-1})$ ',
          xticks = np.arange(0, 1, 0.1))


plt.show()
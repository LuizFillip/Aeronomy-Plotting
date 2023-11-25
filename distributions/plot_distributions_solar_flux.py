import numpy as np
import matplotlib.pyplot as plt
import base as b
import events as ev 
from plotting import plot_distribution



b.config_labels(fontsize = 28)



def plot_distributions_solar_flux(
        df, 
        col = 'gamma',
        level = 86
        ):
    
    
    fig, ax = plt.subplots(
        dpi = 300, 
        sharex = True,
        sharey = True,
        figsize = (13, 6)
        )
        
    labels = [
        '$F_{10.7} < $' + f' {level}',
        '$F_{10.7} > $' + f' {level}'
        ]
    
    if col == 'gamma':
        vmin, vmax, step = 0, 3.2, 0.2
        
    elif col == 'vp':
        vmin, vmax, step = 0, 85, 5
    else:
        vmin, vmax, step = 0, 1, 0.05
    
    solar_dfs =  ev.solar_levels(
        df, 
        level,
        flux_col = 'f107a'
        )
     
    total = []
    
    for i, ds in enumerate(solar_dfs):
    
        c = plot_distribution(
            ax, 
            ds,
            limits = (vmin, vmax, step),
            col = col,
            label = f'{labels[i]}'
            )
        
        total.append(c)
    
    if col == 'vp':
        xlabel = b.y_label('vp')
        vmax = 70
    else:
        xlabel = b.y_label('gamma')
        
        
    ax.set(
        xlim = [vmin, vmax],
        xticks = np.arange(
            vmin, vmax + step, step * 2),
        ylim = [-0.1, 1.1],
        yticks = np.arange(0, 1.25, 0.25),
        )
        
    ax.legend(
        bbox_to_anchor = (0.5, 1.2),
        ncol = 2, 
        loc = 'upper center',
        columnspacing = 0.2
        )
    
    info = f' ({sum(total)} EPBs events)'
    
    ax.set(
        # title = df.columns.name + info,
        xlabel = xlabel, 
        ylabel = 'EPB occurrence probability'
        )
    
    return fig
 

df = ev.concat_results('saa')

col = 'gamma'


# fig = plot_distributions_solar_flux(
#     df, 
#     col, 
#     level = 86
#     )

# FigureName = f'PD_{col}_effects'
vmin, vmax, step = 0, 3.2, 0.2
limits = (vmin, vmax, step)
ds = ev.probability_distribuition(
    df,
    limits,
    col = col
    )

ds.set_index('start', inplace = True)

# def plot_frequency(ax, ds):
    
    
    
    

# fig.savefig(b.LATEX(FigureName), dpi = 400)

# dfs =  ev.solar_levels(
#     df, 
#     level =  86,
#     flux_col = 'f107a'
#     )
import pandas as pd



# ax.set(xticks = ds.index[::2])

ds.index = pd.to_numeric(ds.index)


def plot_hist_distr(ds):
    
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    divider = make_axes_locatable(ax)
    
    xhax = divider.append_axes(
        "top", 
        size=2, pad=0.1, sharex=ax)
    
    yhax = divider.append_axes(
        "right", 
        size = 2, 
        pad = 0.1, 
        
        sharey=ax)
    
    
    args = dict(color = 'gray', 
                edgecolor = 'k')
    xhax.bar(
           ds.index, 
           ds['days'], 
           width = 0.2,
           **args)

    yhax.barh(
        ds.index, 
        ds['epbs'], 
        height = 0.2,
        **args)
    
    ##turning off duplicate ticks:
    plt.setp(xhax.get_xticklabels(), visible=False)
    plt.setp(yhax.get_yticklabels(), visible=False)
    
    
plt.show()


plot_hist_distr(ds)
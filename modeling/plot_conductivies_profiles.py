import base as b
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd 
import datetime as dt 

b.config_labels(fontsize = 35)



df = pd.read_csv('conds', index_col = 0)

df['alt'] = df.index
df.index = pd.to_datetime(df['dn'])

def plot_conductivies_profiles(df):


    fig, ax = plt.subplots(
        ncols = 3, 
        dpi = 300, 
        sharey = True,
        figsize = (16, 10)
        )
    
    plt.subplots_adjust(wspace = 0.1)
    
    cols = ['parl', 'hall', 'perd']
    
    lb = b.labels
    
    times = [
             dt.datetime(2013, 12, 24, 3), 
             dt.datetime(2013, 12, 24, 9),
             dt.datetime(2013, 12, 24, 21)]
    
    factors = [1e6, 1e6 ]
    for dn in times:
        
        limits = [
            [1e-4, 1e9], 
            [1e-2, 1e-12], 
            [1e-9, 1e-2]
            ]
    
        for i, col in enumerate(cols):
            
            ds = df.loc[df.index == dn]
            
            label = dn.strftime('%Hh%M UT')
            
            ax[i].plot(
                ds[col], 
                ds['alt'], 
                label = label,
                lw = 1.5
                )
            
            lim =  limits[i]
            if i == 1:
                f = 1
            else:
                f = 1e2
            # xticks = np.logspace(
            #     np.log10(lim[0] * f), 
            #     np.log10(lim[-1] / f), num = 3)
            
            if i == 0:
                xscale = 'log'
            else:
                xscale = 'linear'
            ax[i].set(
                xscale = 'linear',
                xlabel = b.y_label(col),
                # xlim = lim,
                # xticks = xticks
                )
            
            
    b.plot_letters(ax, y = 0.9, x = 0.05, fontsize = 40)
            
    ax[0].set(ylabel = 'Altitude (km)')
            
    ax[1].legend(
        ncol = 3, 
        title = '24 de dezembro de 2013',
        bbox_to_anchor = (0.5, 1.25),
        loc = "upper center",
        columnspacing = 0.5
        )
    
    return fig

fig = plot_conductivies_profiles(df)
FigureName = 'Conductivities'

fig.savefig(
    b.LATEX(FigureName, 
        folder = 'Iono'),
    dpi = 400
    )


import core as c
import matplotlib.pyplot as plt
import numpy as np
import base as b 
import datetime as dt 


b.config_labels()

def plot_steam_occurrences(df, parameter = 'gamma'):
        
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (16, 8)
        )
    
    ds = df.loc[df['observed'] == df['pred1']]

    ax.stem(ds.index, 
            ds['predict'], linefmt='k-',
            label = 'True'
            )
    
    ds = df.loc[df['observed'] != df['pred1']]

    ax.stem(ds.index, 
            ds['predict'], linefmt='r-',
            label = 'False'
            )
    
    
    ax.legend(
        ncol = 2, 
        bbox_to_anchor = (0.5, 1.1),
        loc = "upper center"
        )
    
    ax.axhline(0.5, color = 'k', lw = 2, linestyle = '--')
    b.format_month_axes(ax, translate = False)
    
    ax.set(
            xlim = [df.index[0], df.index[-1]],
            # yticklabels = np.arange(0, ),
           # xticklabels = b.month_names(),
           ylabel = 'Ocorrência/probabilida (\%)'
           )
    
    ax.text(1.01, 0.25, 'Sem EPB', transform = ax.transAxes)
    ax.text(1.01, 0.75, 'Com EPB', transform = ax.transAxes)
    
    if parameter == 'gamma':
        fig.suptitle('$\\gamma_{RT}$', y = 1.05)
    else:
        fig.suptitle('$V_p$', y = 1.05)
    return fig


def main():
    
    parameter = 'gamma'
    
    df  = c.forecast_epbs(parameter= parameter).data 
    
    fig = plot_steam_occurrences(df, parameter)
    
    plt.show()






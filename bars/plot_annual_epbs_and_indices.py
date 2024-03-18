import matplotlib.pyplot as plt 
import base as b
import core as c
import GEO as gg
import numpy as np 


b.config_labels(fontsize = 25)

args = dict(
    edgecolor = 'black', 
    color = 'gray', 
    linewidth = 1.5
    )


def plot_EPBs(ax, df, col = -50):
    
    ds = c.count_occurences(df).year 
    
    ds[col].plot(
        kind = 'bar', 
        ax = ax, 
        legend = False,
        **args
        )
     
    
    ax.set(
        ylabel = 'Nights with EPB', 
        yticks = list(range(0, 350, 100)),
        xticklabels = []
        )
    
def plot_F107(ax, df, solar_level = 84.33, translate = True):
    
    if translate:
        label = 'Média de 81 dias'
    else:
        label = '81 days average'
        
        
    ax.plot(df['f107'])
        
    ax.plot(
        df['f107a'], 
        lw = 2, 
        label = label
        )
    
    if solar_level is not None:
        ax.axhline(
            solar_level, 
            color = 'r',
            lw = 2, 
            label = f'{solar_level} sfu'
            )
        
    ax.set(
        # xlim = [df.index[0], df.index[-1]],
        ylabel = '$F_{10.7}$ (sfu)', 
        ylim = [50, 300],
        yticks = list(range(50, 350, 50)),
        # xticklabels = []
        )
    
    ax.legend(ncol= 2, loc = 'upper right')

def plot_Kp(ax, df, kp_level = 3, translate = True):
    
    if translate:
        label = 'Média mensal'
        ylabel = 'Índice Kp'
    else:
        label = 'Monthly average'
        ylabel = 'Índice Kp'
    
    ax.bar(df.index, 
           df['kp'], 
           width = 1,
           alpha= 0.7, 
           color = 'gray'
           )
    
    mean = df['kp'].rolling('30D').mean()
    
    ax.set(
        ylabel = ylabel, 
        yticks = list(range(0, 12, 3)
                      )
        )
    
    if kp_level is not None:
        ax.axhline(kp_level, color = 'r', lw = 2)
    
    
    ax.plot(
        mean, label = label,
        lw = 3, 
        color = 'k')
    

    ax.legend(ncol = 2, loc = 'upper right')

def plot_annually_epbs_and_indices(
        df,
        kp_level = 3,
        f107_level = 84.33,
        col = 'epb'
        ):
    
    fig, ax = plt.subplots(
        nrows = 3, 
        dpi = 300, 
        figsize = (14, 12)
        )
    
    plt.subplots_adjust(hspace = 0.1)
   
    plot_EPBs(ax[0], df, col = 'epb')
    
    df.index = df.index.map(gg.year_fraction)

    plot_F107(ax[1], df, solar_level = f107_level)
    plot_Kp(ax[2], df, kp_level = kp_level)

    b.plot_letters(ax, y = 0.83, x = 0.02)
    
    return fig




# df = c.epbs(col = -50, geo = True, eyear = 2022)

# fig = plot_annually_epbs_and_indices(df)

# fig.savefig(b.LATEX('annual_variation', folder = 'bars'))




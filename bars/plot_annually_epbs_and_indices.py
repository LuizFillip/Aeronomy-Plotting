import matplotlib.pyplot as plt 
import base as b
import core as c
import PlasmaBubbles as pb 
import GEO as gg
import numpy as np 


b.config_labels(fontsize = 25)

args = dict(
    edgecolor = 'black', 
    color = 'gray', 
    linewidth = 1.5
    )


def plot_EPBs(ax, df, col = 'epb'):
    
    ds = c.non_and_occurrences(df).yearly()
    
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
    
def plot_F107(ax, df, solar_level = 84.33):
    

    ax.plot(df['f107'])
        
    ax.plot(
        df['f107a'], 
        lw = 2, 
        label = '81 years average')
    
    ax.axhline(
        solar_level, 
        color = 'r',
        lw = 2, 
        label = f'{solar_level} sfu'
        )
    
    ax.set(
        xlim = [df.index[0], df.index[-1]],
        ylabel = '$F_{10.7}$ (sfu)', 
        ylim = [50, 300],
        yticks = list(range(50, 350, 50)),
        xticklabels = []
        )
    
    ax.legend(ncol= 2, loc = 'upper right')

def plot_Kp(ax, df, kp_level = 3):
    
    ax.bar(df.index, 
           df['kp'], 
           width = 0.01,
           alpha= 0.7, 
           color = 'gray'
           )
    
    mean = b.running(df['kp'], 30)
    
    ax.set(
        xlim = [df.index[0], df.index[-1]],
        xticks = np.arange(2013, 2023, 1),
        ylabel = 'Kp index', 
        xlabel = 'Years',
        yticks = list(range(0, 12, 3))
        )
    
    ax.axhline(kp_level, color = 'r', lw = 2)
    
    ax.plot(
        df.index, 
        mean, label = 'Monthly average',
        lw = 3, color = 'k')
    

    ax.legend(ncol = 2, loc = 'upper right')

def plot_annually_epbs_and_indices(
        df,
        kp_level = 3
        ):
    
    fig, ax = plt.subplots(
        nrows = 3, 
        dpi = 300, 
        figsize = (14, 12)
        )
    
    plt.subplots_adjust(hspace = 0.1)
   
    plot_EPBs(ax[0], df)
    solar_level = c.limits_on_parts(df['f107a'], parts = 2)
    
    df.index = df.index.map(gg.year_fraction)

    plot_F107(ax[1], df, solar_level = 84.33)
    plot_Kp(ax[2], df, kp_level = kp_level)

    b.plot_letters(ax, y = 0.83, x = 0.02)
    
    return fig

# df = c.concat_results('saa')
df = c.epbs(geo = True)

fig = plot_annually_epbs_and_indices(df)

fig.savefig(b.LATEX('annual_variation', folder = 'bars'))


import matplotlib.pyplot as plt 
import base as b
import core as c
import GEO as gg 
import numpy as np 
from matplotlib.ticker import AutoMinorLocator
import datetime as dt 

def set_gamma():
    
    dn = dt.time(22, 0)
    
    PATH_GAMMA = 'database/gamma/p1_saa.txt'
    
    df = b.load(PATH_GAMMA)
    
    df = df.loc[df.index.time == dn, ['gamma']] * 1e3
   
    df.index = df.index.normalize()
    
    return c.add_geo(df)

def plot_gamma(ax):
    df = set_gamma()
    
    df_index = c.DisturbedLevels(df)
    
    datasets = df_index.Dst(level = -30, random_state = None)
    clrs = ['gray', 'blue']
    labs = ['Dst $\geq$ -30 nT', 'Dst $<$ -30 nT']
    
    for index, ds in enumerate(datasets):
        
        ds.index = ds.index.map(gg.year_fraction)
        
        ax.scatter(
            ds.index, 
            ds['gamma'], 
            color = clrs[index], 
            label = labs[index]
            )
    
    ylim = [0, 5]
    step = 1
    
    ax.set(
        ylim = ylim, 
        yticks = np.arange(0, ylim[1] + step, step),
        ylabel = b.y_label('gamma')
        )
    
    ax.legend(loc = 'upper right', ncol = 2)
    
    return None

b.config_labels(fontsize = 25)


def plot_EPBs(ax, df, col = -50, translate = True):
    
    df_index = c.DisturbedLevels(df)
    
    datasets = df_index.Dst(level = -30, random_state = None)
    colors = ['gray', 'blue']
    labs = ['Dst $\geq$ -30 nT', 'Dst $<$ -30 nT']
    
    for index, df_level in enumerate(datasets):
        
        ds = c.seasonal_yearly_occurrence(
                df_level, 
                col = col
                )
        ds.index = ds.index.map(gg.year_fraction)
    
        ax.bar(
            ds.index + (index / 10), 
            ds[col], 
            width = 0.08,
            edgecolor = 'black', 
            color = colors[index], 
            alpha = 0.7,
            linewidth = 2,
            label = labs[index]
            )
     
    if translate:
        ylabel = 'Número de casos'
    else:
        ylabel = 'Nights with EPBs'
        
        
    ax.set(
        ylabel = ylabel, 
        yticks = list(range(0, 45, 10)), 
        xlim = [ds.index[0], ds.index[-1]]
        )
    
    ax.legend(
        loc = 'upper right', 
        ncol = 2, 
        # bbox_to_anchor = (0.85, 1.25)
        )
    # ax.legend(loc = 'upper right')
    return ax.get_xlim()
    
    
def plot_F107(
        ax, 
        df, 
        solar_level = None, 
        translate = True, 
        xlim = None
        ):
    
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
        # xlim = xlim,
        ylabel = '$F_{10.7}$ (sfu)', 
        ylim = [40, 300],
        yticks = np.arange(50, 350, 50),
        )
       
    ax.legend(ncol= 2, loc = 'upper right')
    
    plt.xticks(rotation = 0, ha = 'center')
    
    return None 


def plot_storm(
        ax, 
        df, 
        threshold = -30, 
        translate = True, 
        xlim = None
        ):

    ax.bar(
        df.index, 
        df['dst'], 
        width = 0.01,
        alpha = 0.7, 
        color = 'gray'
        )
    
    if threshold is not None:
        ax.axhline(threshold, color = 'r', lw = 2, 
                   label = '-30 nT')
    
        
    ax.set(
        ylim = [-220, 50],
        yticks = [-200, -150, -100, -50, 0, 50],
        ylabel = 'Dst (nT)'
        )
    
    ax.legend(ncol = 2, loc = 'lower right')
    
    return None 


def plot_annually_epbs_and_indices(
        df,
        kp_level = 3,
        f107_level = 84.33,
        col = 'epb',
        translate = False
        ):
    
    fig, ax = plt.subplots(
        nrows = 3, 
        dpi = 300, 
        sharex = True,
        figsize = (14, 12)
        )
    
    plt.subplots_adjust(hspace = 0.1)
 
    plot_EPBs(
        ax[0], df, col = col, 
        translate = translate
        )
    
    # df['Kpmean'] = df['kp'].rolling('30D').mean()
    
    plot_gamma(ax[1])
    
    df.index = df.index.map(gg.year_fraction)
    
    plot_storm(
            ax[-1], 
            df, 
            threshold = -30, 
            translate = True, 
            xlim = None
            )
 

    ax[-1].set(
        xlabel = 'Years',
        xticks = np.arange(2013, 2024, 1), 
        xticklabels = np.arange(2013, 2024, 1), 
    )
    
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator(n=11))
    b.plot_letters(ax, y = 0.85, x = 0.02)
    fig.align_ylabels()
    return fig



def main():
  
    df = c.add_geo(c.epbs())
  
    fig = plot_annually_epbs_and_indices(df)
    
    fig.savefig(b.LATEX('season_annual_on_Dst', folder = 'bars'))



main()



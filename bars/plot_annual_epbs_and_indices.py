import matplotlib.pyplot as plt 
import base as b
import core as c
import GEO as gg 
import numpy as np 
from matplotlib.ticker import AutoMinorLocator
import plotting as pl 
import datetime as dt 
b.config_labels(fontsize = 25)


    

def plot_EPBs(ax, df, col = -50, translate = True):
    
    ds = c.seasonal_yearly_occurrence(
            df, 
            col = col
            )
    ds.index = ds.index.map(gg.year_fraction)

    ax.bar(
        ds.index + 0.1, 
        ds[col], 
        width = 0.08,
        edgecolor = 'black', 
        color = 'gray', 
        alpha = 0.7,
        linewidth = 2
        )
     
    if translate:
        ylabel = 'Número de casos'
    else:
        ylabel = 'Nights with EPB'
        
        
    ax.set(
        ylabel = ylabel, 
        yticks = list(range(0, 45, 10)), 
        xlim = [ds.index[0], ds.index[-1]]
        )
        
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


def plot_Kp(
        ax, 
        df, 
        kp_level = 3, 
        translate = True, 
        xlim = None
        ):
    
    if translate:
        label = 'Média mensal'
        ylabel = 'Índice Kp'
    else:
        label = 'Monthly average'
        ylabel = 'Kp index'
    
    
    ax.bar(
        df.index, 
        df['kp'], 
        width = 0.01,
        alpha = 0.7, 
        color = 'gray'
        )
    
    if kp_level is not None:
        ax.axhline(kp_level, color = 'r', lw = 2)
    
    
    ax.plot(
        df['Kpmean'], label = label,
        lw = 3, 
        color = 'k'
        )
        
    ax.set(
        ylabel = ylabel, 
        yticks = list(range(0, 12, 3))
        )
    
    ax.legend(ncol = 2, loc = 'upper right')

def plot_gamma(ax):
    PATH_GAMMA = 'database/gamma/p1_saa.txt'
    
    df = b.load(PATH_GAMMA)

    df = df.loc[
        (df.index.time == dt.time(22, 0)) & 
        (df.index.year < 2023)]
    
    
    pl.plot_gamma(ax, df['gamma'], avg_run = 27)
    
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
 
    xlim = plot_EPBs(ax[0], df, col = col, translate = translate)
    
    df['Kpmean'] = df['kp'].rolling('30D').mean()
    
    df.index = df.index.map(gg.year_fraction)
    
    plot_F107(
        ax[2], 
        df, 
        solar_level = None,
        translate = translate, 
        xlim = xlim
        )
    
 

    ax[-1].set(
        xlabel = 'Years',
        xticks = np.arange(2013, 2024, 1), 
        xticklabels = np.arange(2013, 2024, 1), 
    )
    
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator(n=11))
    b.plot_letters(ax, y = 0.85, x = 0.02)
    
    return fig



def main():
    df = c.epbs(col = -50, geo = True, eyear = 2022)
    
    fig = plot_annually_epbs_and_indices(df)
    
    # fig.savefig(b.LATEX('annual_variation2', folder = 'bars'))



main()
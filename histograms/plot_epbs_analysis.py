import matplotlib.pyplot as plt 
import numpy as np
import base as b

def figure_labels(fig, fontsize = 30):
     
    fig.text(
        0.3, .63, 
        'Primeira ocorrência (Hora universal)', 
        fontsize = fontsize
        )
    
    fig.text(
        0.3, .35, 
        'Diferença de tempo do anoitecer (horas)', 
        fontsize = fontsize
        )
    
    fig.text(
        0.05, .35, 
        'Frequência de ocorrência', 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    
    fig.text(
        0.35, 0.07, 
        'Período de duração (horas)', 
        fontsize = fontsize
        )

args = dict(
    facecolor='lightgrey', 
    alpha=1, 
    edgecolor = 'black',  
    color = 'gray'
    )




def plot_epbs_stats(
        ds, 
        parameter = 'start', 
        fontsize = 30, 
        n = 24
        ):
    
        
    fig, ax = plt.subplots(
        ncols = 2,
        nrows = 2,
        figsize = (12, 10),
        dpi = 300,
        sharex = True, 
        sharey = True
        )
    
    b.plot_letters(ax, y = 0.83, x = 0.04)
    
    plt.subplots_adjust(wspace = 0.05, hspace = 0.2)
    
    lons = ds['lon'].unique()[::-1]
    
    for i, ax in enumerate(ax.flat):
        
        df = ds.loc[ds['lon'] == lons[i]]
        
        plot_info(ax, df, parameter)

        df[parameter].plot(
            kind = 'hist', 
            ax = ax, 
            bins = b.bins(df, parameter, n), 
            **args
            )
        
        ax.set(title = f'{lons[i]}°')
        
        ax.set( 
            ylabel = '',
            ylim = [0, 400],
            xticks = b.bins(df, parameter, 5)
            )
    
    fig.text( 
        0.4, 0.05,
        'Hora universal'
             , fontsize = fontsize)
    
    fig.text(
        0.03, .32, 'Frequência de ocorrência', 
        rotation = 'vertical', fontsize = fontsize
        )
      
    return fig

def main():
    parameter = 'duration'
    df = b.load('events_2013_2023_2' )
    df = df.loc[~(df['duration'] == 0)|
                  (df['start'] < 21)]
    
    fig = plot_epbs_stats(df, parameter)
    
    FigureName = f'{parameter}_occurrence'
    
    fig.savefig(
        b.LATEX(FigureName, folder = 'histograms'), 
                dpi = 400)



def plot_single_histogram(
        df, 
        parameter = 'start',
        n = 30
        ):

    
    df = df.loc[~((df['duration'] == 0) |
                  (df['start'] < 21))]
    
    
    fig, ax = plt.subplots(
        figsize = (8, 8),
        dpi = 300,
        sharex = True, 
        sharey = True
    
        )
    ds = df.loc[df['lon'] == -50]
    
    ds[parameter].plot(
        kind = 'hist', 
        ax = ax, 
        bins = bins(ds, parameter, n), 
        **args
        )
    
    plot_info(ax, ds, parameter)
    ax.set(xlabel = 'Universal time', 
           title = 'EPBs start time',
           xticks = np.arange(20, 33, 2))
    
    return fig
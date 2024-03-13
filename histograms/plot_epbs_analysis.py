import matplotlib.pyplot as plt 
import numpy as np
import base as b


b.config_labels()
args = dict(
    facecolor='lightgrey', 
    alpha=1, 
    edgecolor = 'black',  
    color = 'gray'
    )


def plot_epbs_stats(ds, fontsize = 30):
    
    
    fig, ax = plt.subplots(
        ncols = 4,
        nrows = 3,
        figsize = (14, 12),
        dpi = 300,
        sharey = 'row'
        )
    
    
    plt.subplots_adjust(wspace = 0.05, hspace = 0.5)
    
    
    for col, lon in enumerate(ds.lon.unique()):
        
        df = ds.loc[ds['lon'] == lon]
        
        df['start'].plot(
            kind = 'hist', 
            ax = ax[0, col], 
            bins = np.arange(20, 30, 0.5), 
            **args
            )
        
        df['shift'].plot(
            kind = 'hist', 
            ax = ax[1, col], 
            bins =  np.arange(-1, 8, 0.5), 
            **args 
            )
        
        df['duration'].plot(
            kind = 'hist', 
            ax = ax[2, col], 
            bins = np.arange(-1, 12, 0.5), 
            **args
            )
        
        ax[0, col].set(title = f'{lon}°')
        
        if col < 3:
            ax[col, 0].set(ylabel = '')
         
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
    
    return fig


df = b.load('events_2013_2023')
df = df.loc[~((df['lon'] == -80) & 
              (df['start'] < 21))]

fig = plot_epbs_stats(df, fontsize = 30)
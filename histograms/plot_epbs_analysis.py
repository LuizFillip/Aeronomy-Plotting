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

b.config_labels()


args = dict(
    facecolor='lightgrey', 
    alpha=1, 
    edgecolor = 'black',  
    color = 'gray'
    )




def plot_info(ax, df, parameter):
    
    vls = df[parameter]
    mu = round(vls.mean(), 1)
    sigma = round(vls.std(), 1)
    
    info =  f'$\mu = $ {mu} horas\n$\sigma = $ {sigma} horas'
    
    ax.text(0.5, 0.7, info, transform = ax.transAxes)
    
def bins(df, parameter = 'start', n = 10):
    vmin = round(df[parameter].min())
    vmax = round(df[parameter].max())

    return np.linspace(vmin, vmax, n)



def plot_epbs_stats(
        ds, 
        parameter = 'start', 
        fontsize = 30
        ):
    
    if parameter == 'start':
        n = 24
    else:
        n = 50
        
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
            bins = bins(df, parameter, n), 
            **args
            )
        
        ax.set(title = f'{lons[i]}°')
        
        ax.set( 
            ylabel = '',
            ylim = [0, 1000],
            xticks = bins(df, parameter, 5)
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


df = b.load('events_2013_2023_2')

fig = plot_epbs_stats(df, fontsize = 30, parameter = 'duration')

# FigureName = 'start_hour_occurrence'

# fig.savefig(b.LATEX(FigureName, folder = 'histograms'), 
#             dpi = 400)

# bins = np.arange(-1, 12, 0.5)


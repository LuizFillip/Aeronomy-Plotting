import core as c
import base as b 
import matplotlib.pyplot as plt 
import numpy as np 


def get_min_max(df):
    
    years = np.unique(df.index.year)
    
    return min(years), max(years)


def plot_seasonal_supression(df):
    
    
    fig, ax = plt.subplots(
        figsize = (12, 6), 
        dpi = 300
        )
    
    ds = c.count_occurences(df).month
    
    vmin, vmax = get_min_max(df)
    
    ds['epb'].plot(
        kind = 'bar',
        ax = ax, 
        color =  'gray',
        legend = False,
        edgecolor = 'k'
        )
    title = f'Supressão de EPBs no setor 1 ({vmin} - {vmax})'
    ax.set(
        ylim = [0, 20],
        ylabel = 'Número de eventos',
        xlabel = 'Meses',
        title = title,
        xticklabels = b.month_names(language = 'pt')
        )
    
    plt.xticks(rotation = 0)
    
    return fig


def main():
    
    lon = -50
    
    df = c.atypical_frame(lon, kind = 0, days = 3)
    print(df)
    fig = plot_seasonal_supression(df)
    
    FigureName = 'seasonality_supression_events'
    
    fig.savefig(
        b.LATEX(FigureName, folder = 'bars'),
        dpi = 400
        )
import core as c
import base as b 
import matplotlib.pyplot as plt 
import numpy as np 

b.config_labels()


def get_min_max(df):
    
    years = np.unique(df.index.year)
    
    return min(years), max(years)


def plot_seasonal_supression(
        df, translate = True):
    
    if translate:
        ylabel = 'Number of cases'
        xlabel = 'Months'
        ln = 'en'
        title = 'EPBs suppressions'
    else:
        ylabel = 'Número de eventos'
        xlabel = 'Meses'
        ln = 'pt'
        title= 'Supressão de EPBs'
        
        
    fig, ax = plt.subplots(
        figsize = (12, 8), 
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
    title = f'{title} ({vmin} - {vmax})'
    ax.set(
        ylim = [0, 20],
        ylabel = ylabel,
        xlabel = xlabel,
        title = title,
        xticklabels = b.month_names(language = ln)
        )
    
    plt.xticks(rotation = 0)
    
    return fig


def main():
    
    lon = -50
    
    df = c.atypical_frame(lon, kind = 0, days = 3)
   
    fig = plot_seasonal_supression(df)
    
    FigureName = 'seasonality_supression_events'
    
    fig.savefig(
        b.LATEX(FigureName, folder = 'bars'),
        dpi = 400
        )
    
# main()
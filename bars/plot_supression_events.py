import core as c
import base as b 
import matplotlib.pyplot as plt 
import numpy as np 

b.config_labels()


def get_min_max(df):
    
    years = np.unique(df.index.year)
    
    return min(years), max(years)


def plot_seasonal_supression(
        df, 
        translate = True
        ):
    
    if translate:
        ylabel = 'Number of cases'
        xlabel = 'Months'
        ln = 'en'
    else:
        ylabel = 'Número de supressões'
        xlabel = 'Meses'
        ln = 'pt'
        title = 'Total de supressões de EPBs (2013 - 2023)'
        
        
    fig, ax = plt.subplots(
        figsize = (16, 10), 
        dpi = 300
        )
    
    df = df[df.columns[::-1]]
    
    df.plot(
        kind = 'bar',
        ax = ax, 
        legend = False,
        edgecolor = 'k'
        )
    ax.set(
        ylim = [0, 30],
        ylabel = ylabel,
        xlabel = xlabel,
        xticklabels = b.month_names(language = ln)
        )
    
    t = [f'Setor {i} ({vl})' for i, vl in 
         enumerate(df.sum().values, start = 1)]
    
    ax.legend(
        t,
        ncol = 5, 
        title = title,
        bbox_to_anchor = (.5, 1.22), 
        loc = "upper center", 
        columnspacing = 0.3,
        fontsize = 28
        )
    
    plt.xticks(rotation = 0)
    
    return fig


def main():
        
    df = c.seasonal_suppression_in_all(kind = 0, days = 3)
        
    fig = plot_seasonal_supression(df, translate = False)
    
    FigureName = 'seasonality_supression_events'
    
    fig.savefig(
        b.LATEX(FigureName, folder = 'bars'),
        dpi = 400
        )
    
# main()
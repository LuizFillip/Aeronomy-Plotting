import core as c
import base as b 
import matplotlib.pyplot as plt 
import numpy as np 

b.sci_format()


def get_min_max(df):
    
    years = np.unique(df.index.year)
    
    return min(years), max(years)

args = dict(  
    edgecolor = 'black', 
    color = 'gray', 
    alpha = 0.7,
    linewidth = 2
    )

def plot_seasonal_suppression(
        df, 
        translate = True
        ):
    
    if translate:
        ylabel = 'Number of cases'
        xlabel = 'Months'
        ln = 'en'
        title = 'Total of EPBs supressions (2013 - 2022)'
    else:
        ylabel = 'Número de supressões'
        xlabel = 'Meses'
        ln = 'pt'
        title = 'Total de supressões de BPEs (2013 - 2022)'
        
        
    fig, ax = plt.subplots(
        figsize = (18, 12), 
        dpi = 300, 
        nrows = 2, 
        sharex = True
        )
    
    plt.subplots_adjust(hspace= 0.1)
    
    df = df[df.columns[::-1]]
   
    df[-50].plot(
        kind = 'bar',
        ax = ax[0], 
        legend = False, **args 
        )
  
    ax[0].set(
        # title = title,
        ylim = [0, 30],
        ylabel = ylabel,
        
        )
    
    df = c.seasonal_storm_events(normalize = False)

    df['dst'].plot(
        kind = 'bar', 
        ax = ax[1], 
        legend = False, 
        **args
        )
    # ax1 = ax[0].twinx()
    
    df['dst'].plot(
        
        # kind = 'bar', 
        # ax = ax[1], 
        # legend = False, 
        # **args
        )

    ax[1].set(
        ylim = [-40, 0],
        ylabel = '$\\overline{Dst}$ (nT)',
        xticklabels = b.month_names(language = ln),
        xlabel = xlabel
        )
    
    a = '(a) Total of EPBs supressions (2013 - 2022)'
    ax[0].text(0.02, 0.85, a, transform = ax[0].transAxes)
    b1 = '(b) Dst index average'
    ax[1].text(0.02, 0.1, b1, transform = ax[1].transAxes)
    
    plt.xticks(rotation = 0)
    fig.align_ylabels()
    return fig


def main():
        
    df = c.seasonal_suppression_in_all(kind = 0, days = 2)
    # print(df)
    fig = plot_seasonal_suppression(df, translate = True)
    
    FigureName = 'seasonality_supression_events_sector_2'
    
    # fig.savefig(
    #     b.LATEX(FigureName, folder = 'bars\en'),
    #     dpi = 400
    #     )
    
# main()

df = c.seasonal_storm_events(normalize = False)

df
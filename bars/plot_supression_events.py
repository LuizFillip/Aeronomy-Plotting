import core as c
import base as b 
import matplotlib.pyplot as plt 
import numpy as np 

b.config_labels()


def get_min_max(df):
    
    years = np.unique(df.index.year)
    
    return min(years), max(years)

args = dict(  edgecolor = 'black', 
  color = 'gray', 
  alpha = 0.7,
  linewidth = 2)

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
        title = 'Total de supressões de EPBs (2013 - 2022)'
        
        
    fig, ax = plt.subplots(
        figsize = (18, 8), 
        dpi = 300
        )
    
    df = df[df.columns[::-1]]
   
    df[-50].plot(
        kind = 'bar',
        ax = ax, 
        legend = False, **args 
        )
    ax.set(
        title = title,
        ylim = [0, 30],
        ylabel = ylabel,
        xlabel = xlabel,
        xticklabels = b.month_names(language = ln)
        )
    
    # t = [f'Setor {i} ({vl})' for i, vl in 
    #      enumerate(df.sum().values, start = 1)]
    
    # ax.legend(
    #     t,
    #     ncol = 5, 
    #     title = title,
    #     bbox_to_anchor = (.5, 1.3), 
    #     loc = "upper center", 
    #     columnspacing = 0.3,
    #     fontsize = 30
    #     )
    
    plt.xticks(rotation = 0)
    
    return fig


def main():
        
    df = c.seasonal_suppression_in_all(kind = 0, days = 2)
    # print(df)
    fig = plot_seasonal_supression(df, translate = False)
    
    FigureName = 'seasonality_supression_events_sector_1'
    
    fig.savefig(
        b.LATEX(FigureName, folder = 'bars'),
        dpi = 400
        )
    
main()
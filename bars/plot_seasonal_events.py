import core as c
import matplotlib.pyplot as plt
import base as b 
import PlasmaBubbles as pb 
import numpy as np 

b.config_labels(blue = False, fontsize = 35)



def plot_seasonal_occurrence(
        ds, 
        typing = 'sunset', 
        translate = False
        ):
    
    ss = pb.sel_typing(ds, typing = 'sunset')
    ds = pb.sel_typing(ds, typing = typing)
    
    e_year = ds.index[-1].year
    s_year = ds.index[0].year
    
   
    ylabel = 'Number of cases'
    xlabel = 'Months'
    sector = 'Sector'
    language = 'en'
    
   
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (18, 8)
        )
    
    ss = c.count_occurences(ss).month
    df = c.count_occurences(ds).month
    cols = [-50, -60, -70]
    
    
    ss = ss[cols].mean(axis = 1).to_frame()
    df = df[cols]
    
    ax1 = ax.twinx()
 
    ax1.plot(ss, color = 'k', linestyle = '--', lw = 3)
    
    ax1.set(
        ylim = [0, 300],
        yticks = np.arange(0, 350, 50),
        ylabel = 'Events of post-sunset EPBs'
        )
    width = 0.2
    
    
    for i, col in enumerate(cols):
        offset = (width) * i 
        
        ax.bar(
            df.index + offset, 
            df[col],
            width = width, 
            edgecolor = 'k',
            )
    plt.xticks(rotation = 0)
    
    
    
    ax.set(
        ylabel = 'Events of midnight EPBs',
        xlabel = xlabel,
        ylim = [0, 150],
        xticks = np.arange(1, 13, 1),
        xticklabels = b.month_names(
            sort = True, language = language),
        
        )
        
    t = [f'{sector} {i} ({vl})' for i, vl in 
         enumerate(df.sum().values, start = 1)]
    
    ax.legend(
        t,
        ncol = 5, 
        title = 'Total of midnight EPBs by sector',
        bbox_to_anchor = (.5, 1.3), 
        loc = "upper center", 
        columnspacing = 0.3,
        fontsize = 35
        )
    
    return fig
    
    
    

def main():

    df = b.load('events_class2')
    df = df.loc[df.index.year < 2023]
    translate = False 
    
    # for typing in ['sunset', 'midnight']:

    typing = 'midnight'
   
    
    fig = plot_seasonal_occurrence(
        df, typing, translate = translate)
    if translate:
        FigureName = f'pt/seasonal_{typing}'
    else:
        FigureName = f'en/seasonal_{typing}'
          
    # fig.savefig(
    #       b.LATEX(FigureName, folder = 'bars'),
    #       dpi = 400
    #       )
   
main()


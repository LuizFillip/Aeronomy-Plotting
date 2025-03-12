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
    
    time = 'month'
    p = pb.BubblesPipe('events_5', 
                       drop_lim = 0.3)
    
    ds = p.sel_type('midnight')
    
   
    ss = p.sel_type('sunset')
    ss = p.time_group(ss, time = time)
  
    ds = p.time_group(ds, time = time)
    

    ylabel = 'Number of cases'
    xlabel = 'Months'
    sector = 'Sector'
    language = 'en'
    
   
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (18, 8)
        )
    
    cols = [-50, -60, -70]
    
    
    ss = ss[cols].mean(axis = 1).to_frame()
    df = ds[cols]
    
    ax1 = ax.twinx()
 
    ax1.plot(
        ss, color = 'k', 
             label = 'post-sunset EPBs',
             linestyle = '--', 
             lw = 3)
    
    ax1.set(
        yticks = np.arange(0, 250, 50),
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
        ylim = [0, 100],
        xticks = np.arange(1, 13, 1),
        xticklabels = b.month_names(
            sort = True, language = language),
        
        )
        
    t = [f'{sector} {i} ({int(vl)})' 
         for i, vl in 
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

    df = b.load('database/epbs/events_class2')
    df = df.loc[df.index.year < 2023]
    translate = False 
    
    # for typing in ['sunset', 'midnight']:

    typing = 'midnight'
   
    
    fig = plot_seasonal_occurrence(
        df, typing, translate = translate)
    if translate:
        FigureName = f'seasonal_{typing}'
    else:
        FigureName = f'seasonal_{typing}'
          
    # fig.savefig(
    #       b.LATEX(FigureName, folder = 'bars'),
    #       dpi = 400
    #       )
    
    save_in = 'G:\\My Drive\\Papers\\Paper 2\\Midnight EPBs\\Eps\\img\\'

    fig.savefig(save_in + FigureName, dpi = 300
                )
    
    
   
main()


import matplotlib.pyplot as plt
import base as b 
import epbs as pb 
import numpy as np 

b.sci_format()

def plot_sunset_curve(ax, ss):
    ax1 = ax.twinx()
    
    color = 'red'
    
    b.change_axes_color(
            ax1, 
            color = color,
            axis = "y", 
            position = "right"
            )
    ax1.plot(
        ss, 
        color = color, 
        label = 'post-sunset EPBs',
        linestyle = '--', 
        lw = 3
        )
    
    ax1.set(
        yticks = np.arange(0, 250, 50),
        ylabel = 'Events of post-sunset EPBs'
        )

def plot_seasonal_occurrence(
        typing = 'sunset', 
        translate = False
        ):
    
    time = 'month'
    infile = 'database/epbs/events_class2' #'events_5'
    p = pb.BubblesPipe(
        infile, 
        drop_lim = 0.3, 
        storm = 'quiet'
        )
    
    ds = p.sel_type(typing)
    
   
    ss = p.sel_type('sunset')
    ss = p.time_group(ss, time = time)
  
    ds = p.time_group(ds, time = time)
    

    xlabel = 'Months'
    sector = 'Sector'
    language = 'en'
    
   
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (16, 8), 
        # nrows = 3, 
        sharex = True, 
        sharey = True
        )
    
    cols = [-50, -60, -70]
    
    
    ss = ss[cols].mean(axis = 1).to_frame()
    df = ds[cols]
    
    plot_sunset_curve(ax, ss)
    
    width = 0.2
    
    
    for i, col in enumerate(cols):
        
        # ax = axs[i]
        
        offset = (width) * i 
        l = b.chars()[i]
        ax.bar(
            df.index + offset, 
            df[col],
            width = width, 
            edgecolor = 'k',
            # color = 'gray'
            )
        
        # ax.text(0.01, 0.8, '{l}')
        
    plt.xticks(rotation = 0)
    
    
    
    ax.set(
        ylabel = 'Events of midnight EPBs',
        xlabel = xlabel,
        ylim = [0, 100],
        xticks = np.arange(1, 13, 1),
        xticklabels = b.month_names(
            sort = True, language = language
        ),
        
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

   
    translate = False 
    
    # for typing in ['sunset', 'midnight']:

    typing = 'midnight'
   
    
    fig = plot_seasonal_occurrence( typing, translate = translate)
    if translate:
        FigureName = f'seasonal_{typing}'
    else:
        FigureName = f'seasonal_{typing}'
          
    # fig.savefig(
    #       b.LATEX(FigureName, folder = 'bars'),
    #       dpi = 400
    #       )
    
    save_in = 'G:\\My Drive\\Papers\\Paper 2\\Midnight EPBs\\Eps\\img\\'
    FigureName = 'abstract'
    # fig.savefig(save_in + FigureName, dpi = 300
    #             )
    
    
   
# main()


# infile = 'database/epbs/events_class2'

# b.


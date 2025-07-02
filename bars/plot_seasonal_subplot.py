

import matplotlib.pyplot as plt
import base as b 
import PlasmaBubbles as pb 
import numpy as np 

b.sci_format()

def plot_sunset_curve(ax, ss):
    ax1 = ax.twinx()
    
    color = 'magenta'
    
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
        
        )
    
    return ax1

def plot_seasonal_occurrence(
        typing = 'sunset', 
        translate = False
        ):
    
    time = 'month'
    p = pb.BubblesPipe(
        'events_5', 
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
    
   
    fig, axs = plt.subplots(
        dpi = 300, 
        figsize = (18, 14), 
        nrows = 3, 
        sharex = True, 
        sharey = True
        )
    
    cols = [-50, -60, -70]
          
    for i, col in enumerate(cols):
        
        ax = axs[i]
        
        l = b.chars()[i]
          
        ax1 = plot_sunset_curve(ax, ss[col])
        ax.bar(
            ds.index, 
            ds[col],
            width = 0.6, 
            edgecolor = 'k',
            color = 'gray'
            )
        sum_pb = int(ds[col].sum())
        
        name = f'({l}) Sector {i + 1} ({sum_pb} EPBs)'
        ax.text(0.01, 0.8, name, 
                transform = ax.transAxes)
        
        if i == 1:
            ylabel = 'Events of post-sunset EPBs'
            ax1.set_ylabel(ylabel)
        
    plt.xticks(rotation = 0)
    
    axs[1].set_ylabel('Events of midnight EPBs')
    axs[-1].set(xlabel = xlabel)
    ax.set(
        
        ylim = [0, 100],
        xticks = np.arange(1, 13, 1),
        xticklabels = b.month_names(
            sort = True, language = language
        ),
        
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
    
    save_in = 'G:\\My Drive\\Papers\\Midnight EPBs\\Eps\\img\\'
    # FigureName = 'abstract'
    # fig.savefig(save_in + FigureName, dpi = 300
    #             )
    
    
   
main()


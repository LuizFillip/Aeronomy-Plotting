import matplotlib.pyplot as plt
import base as b 
import PlasmaBubbles as pb 
import numpy as np 

b.sci_format(blue = False, fontsize = 35)

def set_label(ds, typing, translate = False):
    
 

    
   
    if translate:
        ylabel = 'Número de casos'
        xlabel = 'Anos'
        sector = 'Setor'
        # title = 'Eventos de BPEs'
      
    else:
        ylabel = 'Number of cases'
        xlabel = 'Years'
        sector = 'Sector'
  
    
    return xlabel, ylabel, sector

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
        yticks = np.arange(100, 250, 50),
        ylabel = 'Events of post-sunset EPBs'
        )

def plot_annually_events_count(
        # ds, 
        typing = 'sunset', 
        translate = True
       
        ):
    
    time = 'year'
    p = pb.BubblesPipe(
        'events_5', 
        drop_lim = 0.3, 
        storm = None)
    ss = p.sel_type('sunset')
    ss = p.time_group(ss, time = time)
    
    p = pb.BubblesPipe(
        'events_5', 
        drop_lim = 0.3, 
        storm = 'quiet')
    
    ds = p.sel_type('midnight')
    
    e_year = ds.index[-1].year
    s_year = ds.index[0].year
  
  
    ds = p.time_group(ds, time = time)
    
    
    xlabel, ylabel, sector =  set_label(ds, typing, translate)
    
    

    fig, ax = plt.subplots(
        dpi = 300, 
        sharex = True,
        figsize = (18, 8)
        )
        
    cols = [-50, -60, -70]
    
    ss = ss[cols].mean(axis = 1).to_frame()
    ds = ds[cols]
    
    plot_sunset_curve(ax, ss)
    width = 0.2
    
    
    for i, col in enumerate(cols):
        offset = (width) * i 
        
        ax.bar(
            ds.index + offset, 
            ds[col],
            width = width, 
            edgecolor = 'k',
            )
        
    plt.xticks(rotation = 0)
    
    ax.set(
        ylabel = 'Events of midnight EPBs',
        xlabel = xlabel,
        xticks = np.arange(s_year, e_year + 1, 1),
        ylim = [0, 100]
        )
    
    
    t = [f'{sector} {i} ({vl})' for i, vl in 
          enumerate(ds.sum().values, start = 1)]
    
    ax.legend(
        t,
        ncol = 5, 
        bbox_to_anchor = (.5, 1.3), 
        loc = "upper center", 
        columnspacing = 0.3,
        title = 'Total of midnight EPBs by sector',
        fontsize = 35
        )
    return fig

def main():

    df = b.load('database/epbs/events_class2')
    
    df = df.loc[df.index.year < 2023]
    
    translate = False


    typing = 'midnight'
    if translate:
        FigureName = f'annual_{typing}'
    else:
        FigureName = f'annual_{typing}'
        
    
    
    fig = plot_annually_events_count(
        typing, translate=translate)
    
    save_in = 'G:\\My Drive\\Papers\\Midnight EPBs\\Eps\\img\\'

    fig.savefig(save_in + FigureName, dpi = 300
                )
              
        # fig.savefig(
        #       b.LATEX(FigureName, folder = 'bars'),
        #       dpi = 400
        #       )
        
main()
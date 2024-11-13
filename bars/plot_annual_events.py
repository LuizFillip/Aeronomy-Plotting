import core as c
import matplotlib.pyplot as plt
import base as b 
import PlasmaBubbles as pb 
import numpy as np 

b.config_labels(blue = False, fontsize = 35)

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

def plot_annually_events_count(
        ds, 
        typing = 'sunset', 
        translate = True
       
        ):
    
    ss = pb.sel_typing(ds, typing = 'sunset')
    
    e_year = ds.index[-1].year
    s_year = ds.index[0].year
    
    
    ds = pb.sel_typing(ds, typing = typing)
    
    xlabel, ylabel, sector =  set_label(ds, typing, translate)
    
    if typing == 'sunset':
        vmax = 300
    else:
        vmax = 150
    

    fig, ax = plt.subplots(
        dpi = 300, 
        sharex = True,
        figsize = (18, 8)
        )
        
    df = c.count_occurences(ds).year
    ss = c.count_occurences(ss).year
    cols = [-50, -60, -70]
    
    ss = ss[cols].mean(axis = 1).to_frame()
    df = df[cols]
    
    ax1 = ax.twinx()
 
    ax1.plot(ss, color = 'k', linestyle = '--', lw = 3)
    
    ax1.set(
        ylim = [100, 250],
        yticks = np.arange(100, 300, 50),
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
        xticks = np.arange(s_year, e_year + 1, 1),
        ylim = [0, vmax]
        )
    
    
    t = [f'{sector} {i} ({vl})' for i, vl in 
          enumerate(df.sum().values, start = 1)]
    
    ax.legend(
        t,
        ncol = 5, 
        bbox_to_anchor = (.5, 1.3), 
        loc = "upper center", 
        columnspacing = 0.3,
        title = 'Total of EPBs by sector',
        fontsize = 35
        )
    return fig

def main():

    df = b.load('events_class2')
    
    df = df.loc[df.index.year < 2023]
    
    translate = False


    typing = 'midnight'
    if translate:
        FigureName = f'pt/annual_{typing}'
    else:
        FigureName = f'en/annual_{typing}'
        
    
    
    fig = plot_annually_events_count(
        df, typing, translate=translate)
              
        # fig.savefig(
        #       b.LATEX(FigureName, folder = 'bars'),
        #       dpi = 400
        #       )
        
main()
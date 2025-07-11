import core as c 

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
        marker = 'o',
        markersize = 20,
        fillstyle = 'none',
        label = 'post-sunset EPBs',
        linestyle = '--', 
        lw = 3
        )
    
    ax1.set(
        yticks = np.arange(0, 250, 50),
        
        )
    
    return ax1

def plot_f107(axs):
    df = c.geo_index()

    import GEO as gg
    
    df.index = df.index.map(gg.year_fraction)
    axs[0].plot(df['f107'])
    axs[0].set(xlim = [2013, 2022.5], 
               ylabel = 'F10.7 (sfu)')
    name = '(a) Solar flux'
    axs[0].text(
        0.01, 0.8, name, 
        transform = axs[0].transAxes
        )
def plot_seasonal_occurrence(
        typing = 'sunset',
        time = 'month',
        translate = False
        ):
    

    p = pb.BubblesPipe(
        'events_5', 
        drop_lim = 0.3, 
        storm = 'quiet'
        )
    
    ds = p.sel_type(typing)
    

  
    ds = p.time_group(ds, time = time)
    
    
    if time == 'month':
        nrows = 3
        start = 0
        bc = [
            'gray',
            '#0C5DA5',
            '#00B945', 
        
             ]
    else:
        nrows = 4
        start = 1
        bc = [
            '',
            'gray',
            '#0C5DA5',
            '#00B945', 
        
             ]
   
    fig, axs = plt.subplots(
        dpi = 300, 
        figsize = (14, 14), 
        nrows = nrows, 
        sharex = True, 
        # sharey = True
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    cols = [-50, -60, -70]
          
    for i, col in enumerate(cols, start = start):
        
        ax = axs[i]
        
        l = b.chars()[i]
          
        ax.bar(
            ds.index, 
            ds[col],
            width = 0.4, 
            edgecolor = 'k',
            color = bc[i]
            )
        
        ax.set(ylim = [0, 100])
        sum_pb = int(ds[col].sum())
        
        name = f'({l}) Sector {i + 1} ({sum_pb} EPBs)'
        ax.text(
            0.01, 0.8, name, 
            transform = ax.transAxes
            )
        
    plt.xticks(rotation = 0)
    
    axs[start + 1].set_ylabel('Events of midnight EPBs')
    
    
    if time == 'month':
        ax.set(
            xlabel = 'Months',
            ylim = [0, 100],
            xticks = np.arange(1, 13, 1),
            xticklabels = b.month_names(
                sort = True, 
                language = 'en'
                ),
            
            )
    else:
        plot_f107(axs)
        ax.set(
            xticks = np.arange(2013, 2023, 1),
            xlabel = 'Years'
            )
            
    
    return fig
    
    
    

def main():

   
    translate = False 
    

    typing = 'midnight'
    time = 'month'
    
    fig = plot_seasonal_occurrence( typing, time, translate = translate)
    if translate:
        FigureName = f'seasonal_{typing}'
    else:
        FigureName = f'seasonal_{typing}2'
          

    save_in = 'G:\\My Drive\\Papers\\Midnight EPBs\\Eps\\img\\'
    FigureName = 'annual_midnight2'
    # fig.savefig(save_in + FigureName, dpi = 300
    #             )
    
    
   
# main()


import numpy as np 
import matplotlib.pyplot as plt
import base as b 
import core as c
import PlasmaBubbles as pb 


def plot_annually_both_and_indexes(
        df, 
        xlabel = 'Month', 
        translate = True
        ):
    
    if translate:
        ylabel = 'Número de casos'
        xlabel = 'Anos'
        sector = 'Setor'
    else:
        ylabel = 'Number of cases'
        xlabel = 'Months'
        sector = 'Sector'
    
    
    
    if translate:
        names = ['pós pôr do Sol', 'pós meia noite']
       
    else:
        names = ['Post-sunset',  'Post-midnight']
    
        
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 2,
        sharex = True,
        figsize = (16, 12)
        )
    
    plt.subplots_adjust(hspace = 0.3)
    
    vmax = [350, 150]
    for i, typing in enumerate(['sunset', 'midnight']):
      
        ds = pb.sel_typing(df, typing = typing)
        
        if xlabel == 'years':
            df1 = c.count_occurences(ds).year
            
        else:
            df1 = c.count_occurences(ds).month
           
        
        df1.plot(
            kind = 'bar', 
            ax = ax[i], 
            legend = False
            )
        
        t = [f'{sector} {i} ({vl})' for i, vl in 
             enumerate(df1.sum().values, start = 1)]
        
        ax[i].legend(
            t,
            ncol = 5, 
            title = names[i] + ' EPBs',
            bbox_to_anchor = (.5, 1.3), 
            loc = "upper center", 
            columnspacing = 0.6
            )
        
        ax[i].set(
            ylabel = ylabel,
            xlabel = xlabel.capitalize(),
            ylim = [0, vmax[i]],
            xticklabels = b.month_names(
                sort = True, language = 'en'),
            )
        
    
    plt.xticks(rotation = 0)

    return fig



df = b.load('events_5')

fig = plot_annually_both_and_indexes(
        df,  
        translate = False
        )



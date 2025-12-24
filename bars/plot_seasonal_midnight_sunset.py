import numpy as np 
import matplotlib.pyplot as plt
import base as b 
import core as c
import epbs as pb 

b.sci_format(fontsize = 25)

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
        sharey = True,
        figsize = (16, 12)
        )
    
    plt.subplots_adjust(hspace = 0.2)
    
    ds = pb.sel_typing(df, typing = 'midnight')
    
    datas = [c.count_occurences(ds).month, 
             c.count_occurences(ds).year]
   
    for i, df in enumerate(datas):
        # print(df)
        df.iloc[:, :3].plot(
            kind = 'bar', 
            ax = ax[i], 
            legend = False
            )
        
        t = [f'{sector} {i} ({vl})' for i, vl in 
             enumerate(df.sum().values, start = 1)]
        
        
        ax[i].set(
            ylabel = ylabel,
            xlabel = 'Years',
            # ylim = [0, vmax[i]],
            
            )
        
        ax[i].tick_params(axis='x', labelrotation=0)
        
    ax[0].set(
        xticklabels = b.month_names(
            sort = True, language = 'en'),
        xlabel = xlabel.capitalize()
        )
    
    ax[0].legend(
        t,
        ncol = 5, 
        # title = names[i] + ' EPBs',
        bbox_to_anchor = (.5, 1.3), 
        loc = "upper center", 
        columnspacing = 0.6
        )
    
        

    return fig



df = b.load('database/epbs/events_class2')

fig = plot_annually_both_and_indexes(
        df,  
        translate = False
        )


# df 
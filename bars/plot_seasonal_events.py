import core as c
import matplotlib.pyplot as plt
import base as b 
import PlasmaBubbles as pb 


b.config_labels(fontsize = 25)



def plot_seasonal_occurrence(
        ds, 
        typing = 'sunset', 
        translate = False
        ):
    
    e_year = ds.index[-1].year
    s_year = ds.index[0].year

    
    if typing == 'sunset':
        vmax = 350
        if translate:
            typing = 'pós pôr do Sol'
        else:
            typing = 'Sunset'
        
    else:
        vmax = 150
        if translate:
            typing = 'pós meia noite'
        else:
            typing = 'post-midnight'
        
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 1,
        sharex = True,
        figsize = (16, 6)
        )
    
    plt.subplots_adjust(hspace = 0.1)
        
    df = c.count_occurences(ds).month
    df = df[df.columns[::-1]]
    
    df.plot(kind = 'bar', ax = ax, legend = False)

    plt.xticks(rotation = 0)
    
    if translate:
        ylabel = 'Número de casos'
        xlabel = 'Anos'
        sector = 'Setor'
        title = f'Eventos de EPBs {typing} ({s_year} - {e_year})'
        language = 'pt'
    else:
        ylabel = 'Number of cases'
        xlabel = 'Years'
        sector = 'Sector'
        title = f'Events of {typing} EPBs ({s_year} - {e_year})'
        language = 'en'
    
    ax.set(
        ylabel = ylabel,
        xlabel = xlabel,
        xticklabels = b.month_names(sort = True, language = language),
        ylim = [0, vmax]
        )
        
    t = [f'{sector} {i} ({vl})' for i, vl in 
         enumerate(df.sum().values, start = 1)]
    
    ax.legend(
        t,
        ncol = 5, 
        title = title,
        bbox_to_anchor = (.5, 1.3), 
        loc = "upper center", 
        columnspacing = 0.6
        )
    
    return fig
    
    
    

def main():

    df = b.load('events_class2')
    
    translate = True
    
    for typing in ['sunset', 'midnight']:
     
        
        ds = pb.sel_typing(df, typing = typing)

        fig = plot_seasonal_occurrence(
            ds, typing, translate = translate)
        
        FigureName = f'seasonal_{typing}'
          
        fig.savefig(
              b.LATEX(FigureName, folder = 'bars'),
              dpi = 400
              )
    
# main()

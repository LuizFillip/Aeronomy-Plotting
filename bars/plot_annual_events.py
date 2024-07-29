import core as c
import matplotlib.pyplot as plt
import base as b 
import PlasmaBubbles as pb 


b.config_labels(blue = False, fontsize = 35)


def plot_annually_events_count(
        ds, 
        typing = 'sunset', 
        translate = True
        ):
    
    e_year = ds.index[-1].year
    s_year = ds.index[0].year

    
    if typing == 'sunset':
        vmax = 300
        if translate:
            typing = 'pós-pôr do sol'
        else:
            typing = 'Sunset'
        
    else:
        vmax = 150
        if translate:
            typing = 'pós-meia-noite'
        else:
            typing = 'post-midnight'
        
        
    
    fig, ax = plt.subplots(
        dpi = 300, 
        sharex = True,
        figsize = (18, 8)
        )
        
    df = c.count_occurences(ds).year
    
    # df = df[df.columns[::-1]]
        
    df.plot(
        kind = 'bar', 
        ax = ax, 
        edgecolor = 'k',
        legend = False
        )
    
    plt.xticks(rotation = 0)
    
    if translate:
        ylabel = 'Número de casos'
        xlabel = 'Anos'
        sector = 'Setor'
        title = f'Eventos de EPBs {typing} ({s_year} - {e_year})'
    else:
        ylabel = 'Number of cases'
        xlabel = 'Years'
        sector = 'Sector'
        title = f'Events of {typing} EPBs ({s_year} - {e_year})'
    
    ax.set(
        ylabel = ylabel,
        xlabel = xlabel,
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
        columnspacing = 0.3,
        fontsize = 30
        )
    return fig

def main():
    df = b.load('events_class2')
    
    df = df.loc[df.index.year < 2023]
    
    translate = True
    for typing in ['sunset', 'midnight']:
      
        ds = pb.sel_typing(df, typing = typing)
        
        fig = plot_annually_events_count(
            ds, typing, translate=translate)
        
        FigureName = f'annual_{typing}'
          
        fig.savefig(
              b.LATEX(FigureName, folder = 'bars'),
              dpi = 400
              )
        
# main()
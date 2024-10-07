import core as c
import matplotlib.pyplot as plt
import base as b 
import PlasmaBubbles as pb 


b.config_labels(blue = False, fontsize = 35)


def plot_annually_events_count(
        ds, 
        typing = 'sunset', 
        translate = True, 
        percent = True
        ):
    
    e_year = ds.index[-1].year
    s_year = ds.index[0].year
    
    if translate:
        ylabel = 'Número de casos'
        xlabel = 'Anos'
        sector = 'Setor'
        if typing == 'sunset':
            vmax = 300
            title = f'Eventos de BPEs pós-pôr do sol ({s_year} - {e_year})'
        else:
            vmax = 150
            title = f'Eventos de BPEs próxima da meia-noite ({s_year} - {e_year})'
            
    else:
        ylabel = 'Number of cases'
        xlabel = 'Years'
        sector = 'Sector'
        title = f'Events of {typing} EPBs ({s_year} - {e_year})'
    

    fig, ax = plt.subplots(
        dpi = 300, 
        sharex = True,
        figsize = (18, 8)
        )
        
    df = c.count_occurences(ds).year
    # df = df[[-50, -60, -70]]
    
 
    df.plot(
        kind = 'bar', 
        ax = ax, 
        edgecolor = 'k',
        legend = False
        )
    
    plt.xticks(rotation = 0)
    
    
    
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
    df = b.load('features_one_hour')
    df = b.load('events_class2')
    
    df = df.loc[df.index.year < 2023]
    
    translate = True
    for typing in ['sunset', 'midnight']:
    
        if translate:
            FigureName = f'pt/annual_{typing}'
        else:
            FigureName = f'en/annual_{typing}'
            
        ds = pb.sel_typing(df, typing = typing)
        
        fig = plot_annually_events_count(
            ds, typing, translate=translate)
                  
        fig.savefig(
              b.LATEX(FigureName, folder = 'bars'),
              dpi = 400
              )
        
# main()
import core as c
import matplotlib.pyplot as plt
import base as b 
import PlasmaBubbles as pb 


b.config_labels(fontsize = 25)


def plot_annually_events_count(
        ds, 
        typing = 'sunset'
        ):
    
    e_year = ds.index[-1].year
    s_year = ds.index[0].year

    
    if typing == 'sunset':
        typing = 'pós pôr do Sol'
        vmax = 300
    else:
        typing = 'pós meia noite'
        vmax = 150
    
    fig, ax = plt.subplots(
        dpi = 300, 
        sharex = True,
        figsize = (16, 6)
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    df = c.count_occurences(ds).year
    
    df = df[df.columns[::-1]]
        
    df.plot(
        kind = 'bar', 
        ax = ax, 
        legend = False
        )
    
    plt.xticks(rotation = 0)
    
    ax.set(
        ylabel = 'Número de casos',
        xlabel = 'Anos',
        ylim = [0, vmax]
        )
        
    t = [f'Setor {i} ({vl})' for i, vl in 
         enumerate(df.sum().values, start = 1)]
    
    ax.legend(
        t,
        ncol = 5, 
        title = f'Eventos de EPBs {typing} ({s_year} - {e_year})',
        bbox_to_anchor = (.5, 1.3), 
        loc = "upper center", 
        columnspacing = 0.6
        )
    return fig

def main():
    
    for typing in ['sunset', 'midnight']:
     
        df = b.load('events_class2')
        
        ds = pb.sel_typing(df, typing = typing)
        
        fig = plot_annually_events_count(ds, typing)
        
        FigureName = f'annual_{typing}'
          
        fig.savefig(
              b.LATEX(FigureName, folder = 'bars'),
              dpi = 400
              )
        
main()
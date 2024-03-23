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
        
        name = 'pós pôr do Sol'
        vmax = 400
    else:
        name = 'pós meia noite'
        vmax = 200
    
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
    
    ax.set(
        ylabel = 'Número de casos',
        xlabel = 'Meses',
        xticklabels = b.month_names(sort = True),
        ylim = [0, vmax]
        )
        
    t = [f'Setor {i} ({vl})' for i, vl in 
         enumerate(df.sum().values, start = 1)]
    
    ax.legend(
        t,
        ncol = 5, 
        title = f'Eventos de EPBs {name} ({s_year} - {e_year})',
        bbox_to_anchor = (.5, 1.3), 
        loc = "upper center", 
        columnspacing = 0.6
        )
    
    return fig
    
    
    

def main():
    infile = 'core/data/epb_class'
    infile = 'events_class'
    for typing in ['sunset', 'midnight']:
     
        df = b.load(infile)
        
        ds = pb.sel_typing(df, typing = typing)

        
        fig = plot_seasonal_occurrence(ds, typing)
        
        FigureName = f'seasonal_{typing}'
          
        # fig.savefig(
        #       b.LATEX(FigureName, folder = 'bars'),
        #       dpi = 400
        #       )
    
main()
# infile = 'events_class'
# df = b.load(infile)

# ds = pb.sel_typing(df, typing = 'sunset')

# ds 
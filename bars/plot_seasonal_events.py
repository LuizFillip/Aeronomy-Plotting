import core as c
import matplotlib.pyplot as plt
import base as b 
import PlasmaBubbles as pb 


b.config_labels(fontsize = 25)



def plot_seasonal_occurrence(ds, typing = 'sunset'):
    
    e_year = ds.index[-1].year
    s_year = ds.index[0].year

    
    if typing == 'sunset':
        typing = 'pós pôr do Sol'
    else:
        typing = 'pós meia noite'
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 1,
        sharex = True,
        figsize = (14, 6)
        )
    
    plt.subplots_adjust(hspace = 0.1)
        
    df = c.count_occurences(ds).month
    df = df[df.columns[::-1]]
    
    df.plot(kind = 'bar', ax = ax, legend = False)

    plt.xticks(rotation = 0)
    
    ax.set(
        ylabel = 'Número de casos',
        xlabel = 'Meses',
        xticklabels = b.number_to_months()
        )
        
    t = [f'{col}° ({vl})' for col, vl in 
         zip(df.columns, df.sum().values)]
    
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
     
        df = b.load('core/data/epb_class')
        
        ds = pb.bubble_class(df, typing = 'midnight')

        
        fig = plot_seasonal_occurrence(ds, typing)
        
        FigureName = f'seasonal_{typing}'
          
        # fig.savefig(
        #       b.LATEX(FigureName, folder = 'bars'),
        #       dpi = 400
        #       )
    
main()
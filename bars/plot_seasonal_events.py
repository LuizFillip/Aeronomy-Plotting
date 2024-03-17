import core as c
import matplotlib.pyplot as plt
import base as b 

b.config_labels(fontsize = 25)



def plot_seasonal_occurrence(ds, percent = True):
    
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 1,
        sharex = True,
        figsize = (14, 6)
        )
    
    plt.subplots_adjust(hspace = 0.1)
        
    df = c.CountAllOccurences(ds).month
        
    df.plot(kind = 'bar', ax = ax, legend = False)

    plt.xticks(rotation = 0)
    
    ax.set(
        ylabel = 'Noites com EPB',
        xlabel = 'Meses',
        xticklabels = b.number_to_months()
        )
        
    t = [f'{col}° ({vl})' for col, vl in zip(ds.columns, df.sum().values)]
    
    ax.legend(
        t,
        ncol = 5, 
        title = 'Setores longitudinais e eventos de EPBs (2013 - 2022)',
        bbox_to_anchor = (.5, 1.3), 
        loc = "upper center", 
        columnspacing = 0.6
        )
    
    return fig
    
    
    
def main():
    typing = 'sunset'
    typing = 'postmidnight'

    path = f'database/epbs/{typing}_events2'
    ds = b.load(path)
    
    
    fig = plot_seasonal_occurrence(ds)
    
    FigureName = f'seasonal_{typing}'
    
    # fig.savefig(
    #       b.LATEX(FigureName, folder = 'bars'),
    #       dpi = 400
    #       )
    

# main()
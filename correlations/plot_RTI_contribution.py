import plotting as pl
import core as c 
import matplotlib.pyplot as plt 
import base as b


b.config_labels()

def plot_seasonal_RTI_contribution(
        df, 
        fontsize = 35
        ):
    
    fig, ax = plt.subplots(
        nrows = 2, 
        ncols = 2, 
        sharey = 'row',
        dpi = 300,
        figsize = (16, 12)
        )
    
    plt.subplots_adjust(
        hspace = 0.3,
        wspace = 0.05
        )
    
   
    cols = ['vp', 'K', 'gr', 'mer_perp']
    xlims = [[0, 120], [0, 5], [0, 30], [-8, 8]]
    for i , a in enumerate(ax.flat):
        
        vls = cols[i]
        pl.plot_single_correlation(
            df, 
            ax = a, 
            color = 'k', 
            col = vls,
            index = 0, 
            label = ''
            )
        
    
        a.set(
            xlim = xlims[i],
            xlabel = b.y_label(vls)
            )
    
    
    
    fig.text(
          0.06, 0.4, 
          b.y_label('gamma'), 
          fontsize = fontsize, 
          rotation = 'vertical'
          )
    
   
    
    b.plot_letters(ax, y = 0.85, x = 0.02, fontsize = fontsize)
    return fig


def main():
    
    df = c.load_results('saa', eyear = 2022, 
    gamma_cols = ['vp', 'gamma', 'K', 'gr', 'mer_perp'])
    
    df['K']  = df['K'] *  1e5
    
    fig = plot_seasonal_RTI_contribution(df)
    
    FigureName = 'correlation_all_RTI_terms'
    
    fig.savefig(b.LATEX(
        FigureName, 
        folder = 'correlations'), dpi = 400)
    
# main()
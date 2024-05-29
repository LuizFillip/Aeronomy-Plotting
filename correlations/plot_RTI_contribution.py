import plotting as pl
import core as c 
import matplotlib.pyplot as plt 
import base as b


b.config_labels()

def plot_seasonal_RTI_contribution(
        df, fontsize = 35):
    fig, ax = plt.subplots(
        nrows = 2, 
        ncols = 2, 
        sharey = 'row',
        dpi = 300,
        figsize = (14, 12)
        )
    
    plt.subplots_adjust(
        hspace = 0.25,
        wspace = 0.1
        )
    
   
    cols = ['vp', 'K', 'gr', 'mer_perp']
 
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
        
    
        a.set(xlabel = b.y_label(vls))
    
    
    
    fig.text(
          0.06, 0.4, 
          b.y_label('gamma'), 
          fontsize = fontsize, 
          rotation = 'vertical'
          )
    
   
    
    b.plot_letters(ax, y = 1.04, x = 0.01, num2white = None)
    return fig


def main():
    
    df = c.load_results('saa', eyear = 2022, 
    gamma_cols = ['vp', 'gamma', 'K', 'gr', 'mer_perp'])
    
    df['K']  = df['K'] *  1e5
    
    fig = plot_seasonal_RTI_contribution(df)
    
    FigureName = 'correlation_vp_K_nui'
    
    fig.savefig(b.LATEX(
        FigureName, 
        folder = 'correlations'), dpi = 400)
    
main()
import core as c 
import matplotlib.pyplot as plt 
import base as b


b.config_labels()

def plot_single_correlation(
        df, 
        ax = None, 
        col = 'gamma'
        ):
    
    
    if ax is None:
        fig, ax = plt.subplots(dpi = 300)
        ax.set(ylabel = b.y_label('gamma'), 
               xlabel = b.y_label('vp'))
    
    
    x_vls, y_vls = df['vp'].values, df[col].values
    
    fit = b.linear_fit(x_vls, y_vls)
    
    ax.scatter(x_vls, y_vls, s = 10, c = 'k')
    
    ax.plot(x_vls, fit.y_pred, lw = 2, color = 'red')
    
    a1, b1 = fit.coeficients
    a1, b1 = round(a1, 2), round(b1, 2)
    
    info = f'$\\gamma_{{RT}} = {a1}V_p + {b1}$'
    ax.text(
        0.4, 0.1, info, 
        transform = ax.transAxes
        )
    
    ax.text(
        0.05, 0.85, f'$R^2$ = {fit.r2_score}', 
        transform = ax.transAxes)
    
    if ax is None:
        return fig

def plot_seasonal_gamma_vs_pre(df, col = 'gamma'):

    fig, ax = plt.subplots(
        sharey= 'row', 
        figsize = (14, 12),
        dpi = 300,
        sharex = 'col',
        nrows = 2, 
        ncols = 2
        )
    
    plt.subplots_adjust(wspace = 0.05, hspace = 0.15)
 
    names = ['march', 'june', 'september', 'december']
    
    b.plot_letters(ax, y = 1.04, x = 0.01)
    
    for i, ax in enumerate(ax.flat):
        
        name = names[i]
        
        ds_split = c.SeasonsSplit(df, name)
        
        plot_single_correlation(
            ds_split.sel_season, ax = ax)
    
        ax.set(title = ds_split.name)
    
    fontsize = 30
    fig.text(
         0.04, 0.4, 
         b.y_label('gamma'), 
         fontsize = fontsize, 
         rotation = 'vertical'
         )
     
    fig.text(
         0.45, 0.05, 
         b.y_label('vp'), 
         fontsize = fontsize
         )
    
    
    
    return fig  





def main():
    df = c.concat_results('saa')
    
    fig = plot_seasonal_gamma_vs_pre(df, col = 'gamma')
    
    FigureName = 'seasonal_vp_and_gamma'
     
    fig.savefig(
          b.LATEX(FigureName, folder = 'correlations'),
          dpi = 400
          )


# main()
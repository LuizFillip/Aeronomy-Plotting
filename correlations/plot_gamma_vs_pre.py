import core as c 
import matplotlib.pyplot as plt 
import base as b


b.config_labels()

def plot_infos(ax, fit):
    intercept = round(fit.intercept, 3)
    slope = round(fit.slope[0], 3)
    
    equation = f'$\\gamma_{{RT}} = {slope}V_p + {intercept}$'
    ax.text(
        0.35, 0.08, 
        equation, 
        transform = ax.transAxes
        )
    
    ax.text(
        0.05, 0.85, 
        f'$R^2$ = {fit.r2_score}', 
        transform = ax.transAxes
        )

def plot_scattering(ax, df, col = 'gamma', color = 'k'):
    
    if color == 'k':
        label = 'without EPB'
    else:
        label = 'with EPB'
        
    x_vls, y_vls = df['vp'].values, df[col].values
    
    ax.scatter(x_vls, y_vls, s = 20, c = color, label = label)
    
    return x_vls, y_vls


def plot_labels(fig, fontsize = 30):
    

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
    
    


def plot_single_correlation(
        df, 
        ax = None, 
        col = 'gamma'
        ):
    
    
    if ax is None:
        fig, ax = plt.subplots(
            dpi = 300)
        ax.set(ylabel = b.y_label('gamma'), 
               xlabel = b.y_label('vp'))
    
    
    ds = df.loc[df['epb'] == 1.0]
    x_vls, y_vls = plot_scattering(ax, ds, color = 'k')
    
    # ds = df.loc[df['epb'] == 0.0]
    # plot_scattering(ax, ds, color = 'k')
    
    fit = b.linear_fit(x_vls, y_vls)
    
    ax.plot(x_vls, fit.y_pred, lw = 3, color = 'r')
    

    plot_infos(ax, fit)
      
    if ax is None:
        return fig

def plot_seasonal_gamma_vs_pre(df, col = 'gamma'):

    fig, ax = plt.subplots(
        figsize = (14, 12),
        dpi = 300,
        sharex = True,
        sharey = True,
        nrows = 2, 
        ncols = 2
        )
    
    plt.subplots_adjust(wspace = 0.05, hspace = 0.15)
 
    names = ['march', 'june', 'september', 'december']
    
    b.plot_letters(ax, y = 1.04, x = 0.01)
    
    for i, ax in enumerate(ax.flat):
        
        name = names[i]
        
        ds_split = c.SeasonsSplit(df, name)
                
        plot_single_correlation(ds_split.sel_season, ax = ax)
    
        ax.set(title = ds_split.name)
                 
    plot_labels(fig, fontsize = 30)
            
    return fig  





def main():
    df = c.load_results('saa')
    
    fig = plot_seasonal_gamma_vs_pre(df, col = 'gamma')
    
    FigureName = 'seasonal_vp_and_gamma'
     
    fig.savefig(
          b.LATEX(FigureName, folder = 'correlations'),
          dpi = 400
          )


main()

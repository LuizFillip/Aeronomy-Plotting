import core as c 
import matplotlib.pyplot as plt 
import base as b


b.config_labels()


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
    
    

def plot_infos(ax, fit, i = 0, color = 'k', dep = 'vp'):
    intercept = round(fit.intercept, 2)
    slope = round(fit.slope[0], 2)
    
    if dep == 'vp':
        dep = '$V_P$'
    elif dep == 'K':
        dep = '$K^F$'
    else:
        dep = '$g_e /\\nu_{eff}^F$'

    if intercept < 0: 
        str_int = f'- {abs(intercept)}'
    else:
        str_int = f'+ {intercept}'
        
    if slope < 0:
        str_slp = f'- {abs(slope)}{dep}'
    else:
        str_slp = f'{abs(slope)}{dep}'
    
    equation = '$\gamma_{RT}$ = ' + f'{str_slp}{str_int}'
    
    ax.text(
        0.05, 0.75, 
        f'$R^2$ = {fit.r2_score}\n{equation}', 
        transform = ax.transAxes,
        color = color
        )

def plot_scattering(
        ax, 
        df, 
        col = 'vp', 
        color = 'k', 
        label = ''
        ):
         
    x_vls, y_vls = df[col].values, df['gamma'].values
    
    ax.scatter(
        x_vls, y_vls, 
        s = 20, 
        # alpha = 0.5, 
        c = color, 
        label = label
        )
    
    return x_vls, y_vls




def plot_single_correlation(
        df, 
        ax = None, 
        col = 'gamma',
        color = 'k',
        index = 0,
        label = ''
        ):
    
    
    if ax is None:
        fig, ax = plt.subplots(
            dpi = 300)
        ax.set(ylabel = b.y_label('gamma'), 
               xlabel = b.y_label(col))
    
    
    ds = df.loc[df['epb'] == 1.0]
    x_vls, y_vls = plot_scattering(
        ax, ds, col = col, color = color)
    
    fit = b.linear_fit(x_vls, y_vls)
    
    ax.plot(x_vls, fit.y_pred,
            lw = 3, color = 'red', 
            label = label)
    
    ax.set(ylim = [0, 6])
    plot_infos(
        ax, fit, 
        i = index, 
        dep = col,
        color = color
        )
      
    if ax is None:
        return fig
    
legend_args = dict(
    ncol = 2, 
    loc = 'upper center', 
    labelcolor = 'linecolor',
    bbox_to_anchor = (0.95, 1.3)
    
    )


def plot_seasonal_gamma_vs_pre(
        ax, 
        df, 
        col = 'gamma', 
        color = 'k',
        index = 0,
        label = ''
        ):

    names = ['march', 'june', 'september', 'december']
    
    b.plot_letters(ax, y = 1.04, x = 0.01)
    
    for i, ax in enumerate(ax.flat):
        
        name = names[i]
        
        ds_split = c.SeasonsSplit(df, name)
                
        plot_single_correlation(
            ds_split.sel_season, 
            ax = ax, 
            color = color, 
            index = index, 
            label = label
            )
    
        ax.set(title = ds_split.name)
        
        if i == 0:
            
            ax.legend(**legend_args)
                 
    
            
    return ax

 

def main():
    df = c.load_results('saa', eyear = 2022)
    
    fig = plot_seasonal_gamma_vs_pre(df, col = 'gamma')
    
    FigureName = 'seasonal_vp_and_gamma'
     
    # fig.savefig(
    #       b.LATEX(FigureName, folder = 'correlations'),
    #       dpi = 400
    #       )


# main()

# plot_separe_in_solar_activity()
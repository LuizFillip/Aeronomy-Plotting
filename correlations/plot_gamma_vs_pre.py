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
    
    

def plot_infos(ax, fit, i = 0, color = 'k'):
    intercept = round(fit.intercept, 3)
    slope = round(fit.slope[0], 3)
    
    equation = f'$\\gamma_{{RT}} = {slope}V_p + {intercept}$'
    ax.text(
        0.35, 0.18 - i, 
        equation, 
        transform = ax.transAxes,
        color = color
        )
    
    ax.text(
        0.05, 0.85 - i, 
        f'$R^2$ = {fit.r2_score}', 
        transform = ax.transAxes,
        color = color
        )

def plot_scattering(
        ax, df, 
        col = 'gamma', color = 'k', label = ''):
         
    x_vls, y_vls = df['vp'].values, df[col].values
    
    ax.scatter(
        x_vls, y_vls, 
        s = 20, 
        alpha = 0.5, 
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
               xlabel = b.y_label('vp'))
    
    
    ds = df.loc[df['epb'] == 1.0]
    x_vls, y_vls = plot_scattering(
        ax, ds, color = color)
    
    fit = b.linear_fit(x_vls, y_vls)
    
    ax.plot(x_vls, fit.y_pred, lw = 3, color = color, 
            label = label)

    plot_infos(ax, fit, i = index, color = color)
      
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


def plot_separe_in_solar_activity():

    fig, ax = plt.subplots(
        figsize = (14, 12),
        dpi = 300,
        sharex = True,
        sharey = True,
        nrows = 2, 
        ncols = 2
        )
    
    plt.subplots_adjust(wspace = 0.05, hspace = 0.15)
    
    df = c.load_results('saa', eyear = 2022)
    
    level = c.limits_on_parts(df['f107a'], parts = 2)
    
    df_index = c.DisturbedLevels(df)
    
    F107_labels = df_index.solar_labels(level)
     
    total_epb = []
    total_day = []
    colors = ['k', 'b']
    
    for i, ds in enumerate(df_index.F107(level)):
        
        label =  f'{F107_labels[i]}'
        
        plot_seasonal_gamma_vs_pre(
            ax, ds, 
            col = 'gamma', 
            color = colors[i], 
            index = i * 0.1, 
            label = label
            )
    
    plot_labels(fig, fontsize = 30)
    
    return fig
 

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
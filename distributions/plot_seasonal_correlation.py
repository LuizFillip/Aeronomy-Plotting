import matplotlib.pyplot as plt
import base as b
import core as c 
from plotting import plot_distribution



b.config_labels()



def plot_distributions_solar_flux(
        df, 
        ax,
        col = 'gamma',
        level = 100
        ):
    
    labels = [
        '$F_{10.7} < $' + f' {level}',
        '$F_{10.7} > $' + f' {level}'
        ]
    
    if col == 'gamma':
        vmin, vmax, step = 0, 4, 0.2
        
    elif col == 'vp':
        vmin, vmax, step = 0, 85, 5
    else:
        vmin, vmax, step = 0, 1, 0.05
    
    solar_dfs =  c.solar_levels(
                df, 
                level,
                flux_col = 'f107a'
                )
     
    total = []
    
    for i, ds in enumerate(solar_dfs):
    
        count = plot_distribution(
            ax, 
            ds,
            limits = (vmin, vmax, step),
            col = col,
            label = f'{labels[i]}'
            )
        
        total.append(count)
    
    if col == 'vp':
        xlabel = b.y_label('vp')
        vmax = 70
    else:
        xlabel = b.y_label('gamma')
        
        
    ax.legend( loc = 'lower right')
        
    ax.set(
        xlabel = xlabel, 
        )
    return ax
 



def plot_double_distributions(df):

    fig, ax = plt.subplots(
         dpi = 300, 
         ncols = 2,
         sharey = True,
         figsize = (14, 6)
         )
    
    plt.subplots_adjust(wspace = 0.05)
    
    plot_distributions_solar_flux(
        df, 
        ax[0],
        col = 'vp', 
        level = 86
        )
    
    plot_distributions_solar_flux(
        df, 
        ax[1],
        col = 'gravity', 
        level = 86
        )
    
    ax[0].set(ylabel = 'EPB occurrence probability')
    names = ['Only $V_p$ effects', 
             '$\gamma_{RT}$ with $V_P = 0$']
    
    for i, ax in enumerate(ax.flat):
        
      l = b.chars()[i]
      n = names[i]
      info = f'({l}) {n}'
      
      ax.text(
          0.02, 0.9, info, 
          transform = ax.transAxes
          )
      
    return fig

# df = c.concat_results('saa')


# fig = plot_double_distributions(df)

# FigureName = 'PD_double_effects'

# fig.savefig(b.LATEX(FigureName), dpi = 400)

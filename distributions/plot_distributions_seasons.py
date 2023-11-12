import base as b 
import matplotlib.pyplot as plt 
import events as ev
from plotting import plot_distribution
import numpy as np 

ks = {
      3:  'March equinox',
      6:  'June solstice',
      9:  'Setember equinox',
      12: 'December solstice'
      }

b.config_labels(fontsize = 30)

def plot_single_season(
        ax, 
        solar_dfs,
        month,
        limits,
        name,
        col
        ):
    
    c_event = []
    total = []
    
    
    for i, l in enumerate(solar_dfs):
        
        index = i + 1
        
        ds = ev.seasons(l, month)

        c = plot_distribution(
                ax, 
                ds, 
                limits = limits,
                col = col,
                count = False,
                label = f'({index}) {name[i]}'
                )
        
        total.append(c)
        
        c_event.append(f'({index}) {c} events')
    


    infos = ('EPB occurrence\n' + 
              '\n'.join(c_event))
        
    ax.text(
            0.58, 0.15, 
            infos, 
            transform = ax.transAxes
            )
    
    
    ax.set(
        xlim = [limits[0], limits[1]],
        ylim = [-0.2, 1.4], 
        yticks = np.arange(0, 1.2, 0.25),
        xticks = np.arange(
            limits[0], limits[1] + limits[-1], 0.5)
        )
 
    return ax, total

def plot_distributions_seasons(
        df, 
        col = 'gamma',
        level = 86, 
        fontsize = 38
        ):
    
    fig, ax = plt.subplots(
        ncols = 2,
        nrows = 2, 
        figsize = (18, 10), 
        sharex = True, 
        sharey = True, 
        dpi = 300
        )
    
    plt.subplots_adjust(
        hspace = 0.05, 
        wspace = 0.1
        )
    
    
    if col == 'gamma':
        vmin, vmax, step = 0, 3.5, 0.2
        
    elif col == 'vp':
        vmin, vmax, step = 0, 85, 5
    else:
        vmin, vmax, step = 0, 1, 0.05
        
    limits = (vmin, vmax, step)
    
    
    name = [
        '$F_{10.7} < $' + f' {level}',
        '$F_{10.7} > $' + f' {level}'
        ]
    
    solar_dfs =  ev.solar_levels(
        df, 
        level,
        flux_col = 'f107a'
        )
    
    all_events = []
    
    for j, ax in enumerate(ax.flat):
        
        month = (j + 1) * 3
        
        season_name = ks[month]
        
        ax, total = plot_single_season(
                ax, 
                solar_dfs,
                month,
                limits,
                name,
                col = col
                )
        
        l = b.chars()[j]
        
        all_events.extend(total)
        
        ax.text(
            0.02, 0.85,
            f'({l}) {season_name} ({sum(total)} events)',
            transform = ax.transAxes
            )
        
    ax.legend(
        ncol = 2, 
        bbox_to_anchor = (-.01, 2.3),
        loc = "upper center"
        )
    
    
    fig.text(
        0.05, 0.21, 
        "EPB occurrence probability", 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.42, 0.04, 
        b.y_label('gamma'), 
        fontsize = fontsize
        )
    
    return fig
    

    
df = ev.concat_results('saa')


col = 'gamma'
fig = plot_distributions_seasons(df, col)

FigureName = 'seasonal_all_periods'

fig.savefig(
    b.LATEX(FigureName),
    dpi = 400
    )

def save_figs(df, col = 'gamma'):
    
    names = ['seasonal_quiet', 
             'seasonal_disturbed']
    
    title = ['$Kp \\leq 3$',  '$Kp > 3$']

    for i, FigureName in enumerate(names):
    
        if 'quiet' in FigureName:
            df1 = df.loc[df['kp'] <= 3]
        else:
            df1 = df.loc[df['kp'] > 3]
        
        fig = plot_distributions_seasons(
            df1, col)
        fig.suptitle(title[i], y  = 1.)
        
        fig.savefig(
            b.LATEX(FigureName),
            dpi = 400
            )
        
        
save_figs(df, col = 'gamma')

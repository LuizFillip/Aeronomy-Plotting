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


def plot_single_season(
        ax, 
        solar_dfs,
        month,
        limits,
        name
        
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
            0.65, 0.15, 
            infos, 
            transform = ax.transAxes
            )
    
    
    ax.set(
        xlim = [limits[0], limits[1]],
        ylim = [-0.2, 1.4], 
        yticks = np.arange(0, 1.2, 0.25)
        )
 
    return ax, total

def plot_distributions_seasons(
        df, 
        col = 'gamma',
        level = 86, 
        fontsize = 25
        ):
    
    fig, ax = plt.subplots(
        ncols = 2,
        nrows = 2, 
        figsize = (15, 8), 
        sharex = True, 
        sharey = True, 
        dpi = 300
        )
    
    plt.subplots_adjust(
        hspace = 0.05, 
        wspace = 0.05
        )
    
    
    if col == 'gamma':
        vmin, vmax, step = 0, 4, 0.2
        
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
                name
                )
        
        l = b.chars()[j]
        
        all_events.extend(total)
        
        ax.text(
            0.03, 0.85,
            f'({l}) {season_name} ({sum(total)} events)',
            transform = ax.transAxes
            )
        
    ax.legend(
        ncol = 2, 
        bbox_to_anchor = (-.01, 2.3),
        loc = "upper center"
        )
    
    
    fig.text(
        0.05, 0.3, 
        "EPB occurrence probability", 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.45, 0.05, 
        b.y_label('gamma'), 
        fontsize = fontsize
        )
    
    
    # fig.suptitle(
    #     df.columns.name +
    #     f' ({sum(all_events)} EPBs events)',
    #     y = 1.
    #     )
    
    return fig
    
    


    
df = ev.concat_results('saa')

df['doy'] = df.index.day_of_year.copy()

col = 'gamma'
fig = plot_distributions_seasons(df, col)


# def save_figs():
    
#     for FigureName in ['seasonal_quiet', 
#                         'seasonal_disturbed']:
    
#         if 'quiet' in FigureName:
#             df1 = df.loc[df['kp'] <= 3]
#         else:
#             df1 = df.loc[df['kp'] > 3]
        
#         fig = plot_distributions_seasons(df1, col)
        
#         fig.savefig(
#         b.LATEX(FigureName),
#         dpi = 400
#         )

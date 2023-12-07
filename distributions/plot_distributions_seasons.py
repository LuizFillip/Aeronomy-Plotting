import base as b 
import matplotlib.pyplot as plt 
import core as c
from plotting import plot_distribution

ks = {
      0:  'March equinox',
      1:  'June solstice',
      2:  'September equinox',
      3: 'December solstice'
      }



b.config_labels(fontsize = 20)

def plot_histogram(ax, df ,col):
    
    ds = c.probability_distribuition(
        df,
        col
        )
    
    ds.set_index('start', inplace = True)
    
    ds['days'].plot(
        kind = 'bar', 
        ax  = ax, 
        color = 'gray',
        alpha = 0.3
        )
    
    
    
    return 

def plot_single_histogram(
        ax, 
        solar_dfs,
        month,
        col ='gamma'
        ):
    
    
    for index, dataset in enumerate(solar_dfs):
        
        ds = c.seasons(dataset, month)
        
        plot_histogram(ax, ds, col)

def plot_single_season(
        ax, 
        solar_dfs,
        month,
        name,
        ):
    
    c_event = []
    total = []
    
    
    for index, dataset in enumerate(solar_dfs):
                
        ds = c.seasons(dataset, month)

        count = plot_distribution(
                ax, 
                ds, 
                col,
                count = False,
                label = f'({index + 1}) {name[index]}'
                )
        
        total.append(count)
        
        c_event.append(f'({index}) {c} events')
        
        
    
    infos = ('EPB occurrence\n' + 
              '\n'.join(c_event))
        
    # ax.text(
    #         0.58, 0.15, 
    #         infos, 
    #         transform = ax.transAxes
    #         )
    
    return total

def plot_distributions_seasons(
        df, 
        col = 'gamma',
        level = 86, 
        fontsize = 38
        ):
    
    fig, ax = plt.subplots(
      ncols = 2, 
      nrows = 4,
      figsize = (14, 12), 
      dpi = 300, 
      sharex = 'col'
        )
    
    plt.subplots_adjust(
        hspace = 0.1, 
        wspace = 0.2
        )
    
    solar_name = [
        '$F_{10.7} < $' + f' {level}',
        '$F_{10.7} > $' + f' {level}'
        ]
    
    solar_dfs = c.solar_levels(
        df, 
        level,
        flux_col = 'f107a'
        )
    
    all_events = []
    
    for j in range(4):
        
        season_name = ks[j]
        
        total = plot_single_season(
                ax[j, 0], 
                solar_dfs,
                season_name,
                solar_name
                )
        
      
        all_events.extend(total)
        
        l = b.chars()[j]
        
        ax[j, 0].text(
            0.02, 0.85,
            f'({l}) {season_name} ({sum(total)} events)',
            transform = ax[j, 0].transAxes
            )
        
        plot_single_histogram(
                ax[j, 1], 
                solar_dfs,
                season_name,
                col ='gamma'
                )
        
    ax[0, 0].legend(
        ncol = 2, 
        bbox_to_anchor = (0.5, 1.3),
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

df = c.concat_results('saa')

col = 'gamma'
fig = plot_distributions_seasons(df, col)

FigureName = 'seasonal_all_periods'

# fig.savefig(
#     b.LATEX(FigureName),
#     dpi = 400
#     )
# save_figs(df, col = 'gamma')

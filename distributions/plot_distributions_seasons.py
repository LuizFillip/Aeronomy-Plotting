import base as b 
import matplotlib.pyplot as plt 
import core as c
import plotting as pl 


ks = {
      0: 'March equinox',
      1: 'June solstice',
      2: 'September equinox',
      3: 'December solstice'
      }



b.config_labels(fontsize = 20)


def plot_single_season(
        ax1, 
        ax2,
        solar_dfs,
        month,
        name,
        ):
    
    total_epb = []
    total_day = []
    
    for i, dataset in enumerate(solar_dfs):
                
        ds = c.seasons(dataset, month)
        index = i + 1
        
        label = f'({index}) {name[i]}'
        
        epbs = pl.plot_distribution(
                ax1, 
                ds, 
                col,
                count = False,
                label = label
                )
        
        days = pl.plot_histogram(
                ax2, 
                ds, 
                index, 
                label = label
                )
        
        total_epb.append(epbs)
        total_day.append(days)

    return total_epb, total_day


def plot_distributions_seasons(
        df, 
        col = 'gamma',
        level = 86, 
        fontsize = 30
        ):
    
    nrows = 4
    
    fig, ax = plt.subplots(
          ncols = nrows // 2, 
          nrows = nrows,
          figsize = (16, 12), 
          dpi = 300, 
          sharex = 'col', 
          sharey = 'col'
        )
    
    plt.subplots_adjust(
        hspace = 0.1, 
        wspace = 0.2
        )
    
    solar_name = [
        '$F_{10.7} \\leq $' + f' {level}',
        '$F_{10.7} > $' + f' {level}'
        ]
    
    solar_dfs = c.solar_levels(
        df, 
        level,
        flux_col = 'f107a'
        )
    
    total = []
    for row in range(nrows):
        
        season_name = ks[row]
        
        epb, day = plot_single_season(
                ax[row, 0], 
                ax[row, 1],
                solar_dfs,
                season_name,
                solar_name
                )
        
        total.extend(day)
        
        pl.plot_infos(
            ax[row, 0], epb, x = 0.65
            )
        pl.plot_infos(
            ax[row, 1], day, x = 0.65,
            title = '$\gamma_{RT}$ total'
            )
    
    
        l = b.chars()[row]
        
        ax[row, 0].text(
            0.02, 0.85,
            f'({l}) {season_name}',
            transform = ax[row, 0].transAxes
            )
        
        ax[row, 1].text(
            0.02, 0.85,
            f'{season_name}',
            transform = ax[row, 1].transAxes
            )
    
    ax[0, 0].legend(
        ncol = 2, 
        columnspacing = 0.3,
        bbox_to_anchor = (0.5, 1.3),
        loc = "upper center"
        )
    
    ax[0, 1].legend(
        ncol = 2, 
        columnspacing = 0.3,
        bbox_to_anchor = (0.5, 1.3),
        loc = "upper center"
        )
    
    
    fig.text(
        0.05, 0.35, 
        "EPB occurrence probability", 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.49, 0.35, 
        "Frequency of occurrence", 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.42, 0.07, 
        b.y_label('gamma'), 
        fontsize = fontsize
        )
    
    ax[0, 1].set(ylim = [0, 200])
    
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
        
        fig = plot_distributions_seasons(df1, col)
        
        fig.suptitle(title[i], y = 0.95)
        
        fig.savefig(
            b.LATEX(FigureName),
            dpi = 400
            )

df = c.concat_results('saa')

col = 'gamma'

limit = c.limits_on_parts(
    df['f107a'], parts = 2)

# fig = plot_distributions_seasons(
#     df, col, level = 83.66)

# FigureName = 'seasonal_all_periods'

# fig.savefig(
#     b.LATEX(FigureName),
#     dpi = 400
#     )

save_figs(df, col = 'gamma')




import base as b 
import matplotlib.pyplot as plt 
import core as c
import plotting as pl 



b.config_labels(fontsize = 20)

    
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

def solar_labels(level):
    return [
    '$F_{10.7} \\leq $' + f' {level}',
    '$F_{10.7} > $' + f' {level}'
    ]        


def FigureLabels(
        fig, 
        translate = False, 
        fontsize = 30
        ):
    if translate:
        ylabel1 = "EPB occurrence probability"
        ylabel2 = "Frequency of occurrence"
        
    else:
        ylabel1 = "Probabilidade de ocorrência das EPBs"
        ylabel2 = "Frequência de ocorrência"
        
    fig.text(
        0.05, 0.35, 
        ylabel1, 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.5, 0.37, 
        ylabel2, 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.42, 0.07, 
        b.y_label('gamma'), 
        fontsize = fontsize
        )
        
def plot_single_season(
        col,
        ax1,
        solar_dfs,
        season_name, 
        ax2 = None,
        level = 84.33
        ):
    
    total_epb = []
    total_day = []
    
    solar_name = solar_labels(level)
    
    for i, dataset in enumerate(solar_dfs):
                
        ds = c.seasons(dataset, season_name)
        index = i + 1
        
        label = f'({index}) {solar_name[i]}'
        
        ds1, epbs = pl.plot_distribution(
                ax1, 
                ds, 
                col,
                count = False,
                label = label
                )
                
        total_epb.append(epbs)
        
        if ax2 is not None:
            days = pl.plot_histogram(
                    ax2, 
                    ds, 
                    index, 
                    label = label
                    )
            total_day.append(days)
            
        
            
    if ax2 is not None:
        return total_epb, total_day
    else:
        return total_epb, total_day
    

def plot_distributions_seasons(
        df, 
        col,
        level = 86
        ):
    
    nrows = 4
    
    fig, ax = plt.subplots(
          ncols = nrows // 2, 
          nrows = nrows,
          figsize = (18, 14), 
          dpi = 300, 
          sharex = 'col', 
          sharey = 'col'
        )
    
    plt.subplots_adjust(
        hspace = 0.1, 
        wspace = 0.18
        )
    
    
    solar_dfs = c.solar_levels(
        df, 
        level,
        flux_col = 'f107a'
        )
    
    total = []
    for row, season_name in enumerate(pl.seasons_keys.values()):
        
        
        epb, day = plot_single_season(
                col,
                ax1 = ax[row, 0], 
                ax2 = ax[row, 1],
                solar_dfs = solar_dfs,
                season_name = season_name, 
                level = level
                )
        
        total.extend(day)
        
        pl.plot_infos(
            ax[row, 0], epb, x = 0.68, 
            y = 0.2
            )
        pl.plot_infos(
            ax[row, 1], day, x = 0.68, 
            y = 0.2,
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
    
    FigureLabels(
        fig, 
        translate = True, 
        fontsize = 30
        )
    
    ax[0, 1].set(ylim = [0, 300])
    
    return fig

def main():
    
    df = c.concat_results('saa')
    
    col = 'gamma'
    
    limit = c.limits_on_parts(
        df['f107a'], parts = 2)
    
    fig = plot_distributions_seasons(
        df, col, level = limit)
    
    FigureName = 'seasonal_all_periods'
    
    fig.savefig(
        b.LATEX(FigureName, folder = 'distributions/pt/'),
        dpi = 400
        )
    
    save_figs(df, col = 'gamma')
    
        
    
# main()
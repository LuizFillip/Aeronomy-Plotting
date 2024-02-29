import matplotlib.pyplot as plt
import base as b
import core as c
import plotting as pl


b.config_labels(fontsize = 25)


def plot_storm_levels_distribution(
        df, 
        nrows = 4,
        level = 86, 
        fontsize = 30,
        translate = False
        ):
    
    quiet_level = 3 
    titles = [
        f'$Kp \\leq$ {quiet_level}', 
        f'$Kp >$ {quiet_level}']
    
    
    fig, ax = plt.subplots(
          ncols = nrows // 2, 
          nrows = nrows,
          figsize = (18, 14), 
          dpi = 300, 
          sharex = 'col', 
          sharey = 'row'
        )
    
    plt.subplots_adjust(
        hspace = 0.1, 
        wspace = 0.05
        )
    
    for col, df_disturb in enumerate(c.kp_levels(df)):
                                    
    
        solar_dfs = c.solar_levels(
            df_disturb, 
            level,
            flux_col = 'f107a'
            )
        
        ax[0, col].set(title = titles[col])
        
        for row, season_name in enumerate(pl.seasons_keys.values()):
            
            epb, _ = pl.plot_single_season(
                    col = 'gamma',
                    ax1 = ax[row, col], 
                    ax2 = None,
                    solar_dfs = solar_dfs,
                    season_name = season_name, 
                    level = level
                    )
                    
         
            pl.plot_infos(
                ax[row, col], epb, 
                x = 0.65, 
                y = 0.2
                )
            
    
            l = b.chars()[row]
            
            y = 0.82
            x = 0.02
            ax[row, 0].text(
                x, y,
                f'({l}) {season_name}',
                transform = ax[row, 0].transAxes
                )
            
            ax[row, 1].text(
                x, y,
                f'{season_name}',
                transform = ax[row, 1].transAxes
                )
        
    
    ax[0, 0].legend(
        ncol = 2, 
        bbox_to_anchor = (1., 1.6),
        loc = "upper center"
        )
    
    if translate:
        ylabel = 'Probabilidade de ocorrência'
    else:
        ylabel = 'Occurrence Probability'
        
    fig.text(
        0.05, 0.25, 
        ylabel, 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.45, 0.07, 
        b.y_label('gamma'), 
        fontsize = fontsize
        )
        
    return fig


def main():

    df = c.concat_results('saa')
    
    limit = c.limits_on_parts(
        df['f107a'], parts = 2
        )
        
    fig = plot_storm_levels_distribution(
        df, level = limit, 
        translate = True)
    
    
    FigureName = 'seasonal_quiet_disturbed'
    
    fig.savefig(
        b.LATEX(FigureName, 
                folder = 'distributions/pt/'),
        dpi = 400
        )
    
    
# main()
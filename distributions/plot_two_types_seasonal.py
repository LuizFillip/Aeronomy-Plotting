import base as b 
import matplotlib.pyplot as plt 
import core as c
import plotting as pl 


b.config_labels(fontsize = 25)

def plot_distributions_seasons(
        df, 
        level = 86, 
        fontsize = 30,
        translate = False
        ):
    
    nrows = 4
    
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
    
    
    solar_dfs = c.solar_levels(
        df, 
        level,
        flux_col = 'f107a'
        )
    
    
    for row, season_name in enumerate(pl.seasons_keys.values()):
        
        
        epb, _ = pl.plot_single_season(
                col = 'gamma',
                ax1 = ax[row, 0], 
                ax2 = None,
                solar_dfs = solar_dfs,
                season_name = season_name, 
                level = level
                )
        
        # print(epb)
        
        _ = pl.plot_single_season(
                col = 'vp',
                ax1 = ax[row, 1], 
                ax2 = None,
                solar_dfs = solar_dfs,
                season_name = season_name, 
                level = level
                )
        
        pl.plot_infos(
            ax[row, 0], epb, 
            x = 0.65, 
            y = 0.2
            )
        
    
        y = 0.80
        ax[row, 0].text(
            0.02, y,
            f'{season_name}',
            transform = ax[row, 0].transAxes
            )
        
        ax[row, 1].text(
            0.02, y,
            f'{season_name}',
            transform = ax[row, 1].transAxes
            )
        
    
    ax[0, 0].legend(
        ncol = 2, 
        bbox_to_anchor = (1., 1.5),
        loc = "upper center"
        )
    
    if translate:
        ylabel = 'Probabilidade de ocorrência das EPBs'
    else:
        ylabel = 'EPB occurrence Probability'
    
    fig.text(
        0.05, 0.35, 
        ylabel, 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    ax[-1, 0].set(xlabel = b.y_label('gamma'))
    ax[-1, 1].set(xlabel = b.y_label('vp'))
    
    ax[0, 0].text(0, 1.05, '(a)', fontsize = 30, 
                  transform = ax[0, 0].transAxes)
    ax[0, 1].text(0, 1.05, '(b)', fontsize = 30, 
                  transform = ax[0, 1].transAxes)
    return fig


def main():    
    df = c.concat_results('saa')
    
    limit = c.limits_on_parts(
        df['f107a'], parts = 2
        )
        
    fig = plot_distributions_seasons(
            df, 
            level = limit, 
            fontsize = 30,
            translate = True
            )
    
    FigureName = 'seasonal_gamma_and_vp'
    
    fig.savefig(
        b.LATEX(FigureName, 
                folder = 'distributions/pt/'),
        dpi = 400
        )
    
main()
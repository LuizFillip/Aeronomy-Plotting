import base as b 
import matplotlib.pyplot as plt 
import core as c
import plotting as pl 


b.config_labels(fontsize = 25)

def plot_distributions_seasons(
        df, 
        limit = 86, 
        fontsize = 30,
        translate = False,
        drop_ones = True
        ):
        
    fig, ax = plt.subplots(
          ncols =  2, 
          nrows = 4,
          figsize = (18, 14), 
          dpi = 300, 
          sharex = 'col', 
          sharey = 'row'
        )
    
    plt.subplots_adjust(
        hspace = 0.1, 
        wspace = 0.05
        )
    

    names = ['march', 'june', 'september', 'december']
    
    
    for row, name in enumerate(names):
        
        df_season = c.SeasonsSplit(df, name)
        
        df_index = c.DisturbedLevels(df_season.sel_season)
        
        F107_labels = df_index.solar_labels(limit)
        
        for index, df_level in enumerate(df_index.F107(limit)):
    
            _, epb = pl.plot_distribution(
                     ax[row, 0], 
                     df_level, 
                     parameter = 'gamma',
                     label = F107_labels[index],
                     drop_ones = drop_ones,
                     season = name
                     )
             
            _, epb = pl.plot_distribution(
                     ax[row, 1], 
                     df_level, 
                     parameter = 'vp',
                     label = F107_labels[index],
                     drop_ones = drop_ones,
                     season = name
                     )
             
            
        
            y = 0.80
            ax[row, 0].text(
                0.02, y,
                f'{df_season.name}',
                transform = ax[row, 0].transAxes
                )
            
            ax[row, 1].text(
                0.02, y,
                f'{df_season.name}',
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
        ylabel = 'EPB occurrence Probability (\%)'
    
    fig.text(
        0.05, 0.35, 
        ylabel, 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    ax[-1, 0].set(xlabel = b.y_label('gamma'))
    ax[-1, 1].set(xlabel = b.y_label('vp'))
    
    ax[0, 0].text(
        0, 1.05, '(a)', 
        fontsize = fontsize, 
        transform = ax[0, 0].transAxes
        )
    ax[0, 1].text(
        0, 1.05, '(b)', 
        fontsize = fontsize, 
        transform = ax[0, 1].transAxes
        )
    return fig


def main():    
    df = c.concat_results('saa')
    
    limit = c.limits_on_parts(
        df['f107a'], parts = 2
        )
        
    fig = plot_distributions_seasons(
            df, 
            limit = limit, 
            fontsize = 30,
            translate = False
            )
    
    FigureName = 'seasonal_gamma_and_vp'
    
    fig.savefig(
        b.LATEX(FigureName, 
                folder = 'distributions/pt/'),
        dpi = 400
        )
    
main()
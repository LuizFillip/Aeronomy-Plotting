import matplotlib.pyplot as plt
import base as b
import core as c 
import plotting as pl



b.config_labels(fontsize= 25)

def plot_labels(fig, ax, fontsize = 30, translate = False ):
   

    if translate:
        ylabel = 'Probabilidade de ocorrência das EPBs'
    else:
        ylabel = 'EPB occurrence Probability (\%)'
    
    fig.text(
        0.05, 0.33, 
        ylabel, 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.49, 0.43, 
        b.y_label('gamma'), 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    
    fig.text(
        0.48, 0.05, 
        b.y_label('vp'), 
        fontsize = fontsize
        )
    
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

def plot_seasonal_correlation(
        df, 
        limit, 
        parameter = 'vp',
        translate = False, 
        drop_ones = True
        ):
    

    fig, ax = plt.subplots(
          ncols =  2, 
          nrows = 4,
          figsize = (18, 14), 
          dpi = 300, 
          sharex = True, 
          sharey = 'col', 
        )
    
    plt.subplots_adjust(
        hspace = 0.1, 
        wspace = 0.2
        )
    
    
    names = ['march', 'june', 'september', 'december']
    
    
    for row, name in enumerate(names):
        
        df_season = c.SeasonsSplit(df, name, translate = translate)
        
        df_index = c.DisturbedLevels(df_season.sel_season)
        
        F107_labels = df_index.solar_labels(limit)
        
        pl.plot_single_correlation(
            df_season.sel_season, 
            ax =  ax[row, 1], 
            col = 'gamma'
            )
        
        ax[row, 1].set(ylim  = [0, 3.2])
        
        for index, df_level in enumerate(df_index.F107(limit)):
        
            ds, epb = pl.plot_distribution(
                     ax[row, 0], 
                     df_level, 
                     parameter = parameter,
                     label = F107_labels[index],
                     drop_ones = drop_ones,
                     season = name
                     )
            
        
            y = 0.80
            x = 0.05
            ax[row, 0].text(x, y,
                f'{df_season.name}',
                transform = ax[row, 0].transAxes
                    )
            
            ax[row, 1].text(x, y,
                f'{df_season.name}',
                transform = ax[row, 1].transAxes
                )
     
    plot_labels(fig, ax, fontsize = 30, translate = False )
    
    return fig


df = c.concat_results('saa')
 
limit = c.limits_on_parts(
     df['f107a'], parts = 2
     )
fig = plot_seasonal_correlation(df, limit)

FigureName = 'seasonal_vp_correlation'
 
# fig.savefig(
#       b.LATEX(FigureName, folder = 'distributions/en/'),
#       dpi = 400
#       )

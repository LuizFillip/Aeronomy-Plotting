import matplotlib.pyplot as plt
import base as b
import core as c 
import plotting as pl



b.config_labels()


drop_ones = True 

df = c.concat_results('saa')
 
limit = c.limits_on_parts(
     df['f107a'], parts = 2
     )

fig, ax = plt.subplots(
      ncols =  2, 
      nrows = 4,
      figsize = (18, 14), 
      dpi = 300, 
      sharex = 'col', 
      sharey = 'col', 
    )

plt.subplots_adjust(
    hspace = 0.1, 
    wspace = 0.2
    )


names = ['march', 'june', 'september', 'december']


for row, name in enumerate(names):
    
    df_season = c.SeasonsSplit(df, name)
    
    df_index = c.DisturbedLevels(df_season.sel_season)
    
    F107_labels = df_index.solar_labels(limit)
    
    pl.plot_single_correlation(
        df_season.sel_season, 
        ax =  ax[row, 1], 
        col = 'gamma'
        )
    
    for index, df_level in enumerate(df_index.F107(limit)):
    
        _, epb = pl.plot_distribution(
                 ax[row, 0], 
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
        
fontsize = 30     
# if translate:
#     ylabel = 'Probabilidade de ocorrência das EPBs'
# else:
ylabel = 'EPB occurrence Probability (\%)'

fig.text(
    0.05, 0.35, 
    ylabel, 
    fontsize = fontsize, 
    rotation = 'vertical'
    )

ax[-1, 0].set(xlabel = b.y_label('vp'))
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
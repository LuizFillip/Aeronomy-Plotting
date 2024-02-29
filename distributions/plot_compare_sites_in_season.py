import matplotlib.pyplot as plt
import base as b
import core as c
import plotting as pl

def set_data(year):    
    ds = c.local_results(year)
    
    df = c.concat_results('saa')
    
    df = df.loc[df.index.year == year]
    
    return df, ds

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
    wspace = 0.05
    )

                                
titles = ['Jicamarca', 'São Luís']
parameter = 'gamma'

names = ['march', 'june', 'september', 'december']


total_epb = []
total_day = []
year = 2013


for index, df in enumerate(set_data(year)):
    
    for row, name in enumerate(names):
        
        df_season = c.SeasonsSplit(df, name).sel_season
    
        ds, epb = pl.plot_distribution(
                ax[row, 0], 
                df_season, 
                parameter,
                label = titles[index]
                )
        
        total_epb.append(epb)
        
        days = pl.plot_histogram(
                ax[row, 1], 
                ds, 
                index,
                label = titles[index]
                )
        total_day.append(days)
                
        ax[row, index].text(
            0.07, 0.82,
            f'{df_season.name}',
            transform = ax[row, index].transAxes
            )
    
    LIST = [total_epb, total_day]
    pl.plot_events_infos(ax, row, LIST)
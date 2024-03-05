import matplotlib.pyplot as plt
import core as c
import plotting as pl

def set_data(year, wind = -20):    
    jic = c.local_results(year)
    
    df = c.concat_results('saa')
    
    saa = df.loc[df.index.year == year]
    
    return saa, jic


def plot_compare_sites_in_season(
        parameter = 'gamma'
        ):
    fig, ax = plt.subplots(
          ncols = 2,
          nrows = 4,
          figsize = (20, 14), 
          dpi = 300, 
          sharex = 'col', 
          sharey = 'col'
        )
    
    plt.subplots_adjust(
        hspace = 0.1, 
        wspace = 0.2
        )
    
                                    
    titles = [ 'São Luís', 'Jicamarca']
    
    names = ['march', 'june', 'september', 'december']
    
    for row, name in enumerate(names):
    
        total_epb = []
        total_day = []
        
        for index, df in enumerate(c.get_same_length()):
            
            df_season = c.SeasonsSplit(df, name)
        
            ds, epb = pl.plot_distribution(
                    ax[row, 0], 
                    df_season.sel_season, 
                    parameter,
                    label = titles[index],
                    drop_ones = True
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
    
    # fig.suptitle(year)
    
    pl.FigureLabels(
            fig, 
            translate = False, 
            fontsize = 30
            )
    plt.show()
    return fig

# for year in range(2013, 2021):

fig = plot_compare_sites_in_season(
        parameter = 'gamma'
        )

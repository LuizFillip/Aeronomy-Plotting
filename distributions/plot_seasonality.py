import base as b 
import matplotlib.pyplot as plt 
import core as c
import plotting as pl 



b.config_labels(fontsize = 25)


        
def FigureAxes(nrows = 4):
    
    fig, ax = plt.subplots(
          ncols = nrows // 2, 
          nrows = nrows,
          figsize = (20, 14), 
          dpi = 300, 
          sharex = 'col', 
          sharey = 'col'
        )
    
    plt.subplots_adjust(
        hspace = 0.1, 
        wspace = 0.18
        )
    
    return fig, ax 



def plot_distributions_seasons(
        df, 
        parameter = 'gamma',
        limit = 86, 
        translate = False
        ):
    
    fig, ax = FigureAxes()

    names = ['march', 'june', 'september', 'december']
    
    
    for row, name in enumerate(names):
        
        total_epb = []
        total_day = []
        
        
        df_season = c.SeasonsSplit(df, name)
        
        df_index = c.DisturbedLevels(df_season.sel_season)
        
        F107_labels = df_index.solar_labels(limit)
        
        for index, df_level in enumerate(df_index.F107(limit)):
    
            data, epb = pl.plot_distribution(
                    ax[row, 0], 
                    df_level, 
                    parameter,
                    label = F107_labels[index],
                    drop_ones = True, 
                    translate = translate
                    )
            
            total_epb.append(epb)
            
            days = pl.plot_histogram(
                    ax[row, 1], 
                    data, 
                    index,
                    parameter = parameter,
                    label = F107_labels[index]
                    )
            
            total_day.append(days)
            
            ax[row, 1].set(ylim = [0, 300])
                    
            ax[row, index].text(
                0.07, 0.82,
                f'{df_season.name}',
                transform = ax[row, index].transAxes
                )
            
        
        
        LIST = [total_epb, total_day]
        pl.plot_events_infos(
            ax, row, LIST, 
            translate = translate
            )
            
        
    pl.FigureLabels(
        fig, 
        translate = translate, 
        fontsize = 30
        )
    
    return fig


def main():

    parameter = 'gamma'
    df = c.concat_results('saa')
    limit = c.limits_on_parts(df['f107a'])
    
    fig = plot_distributions_seasons(
            df, 
            parameter = parameter,
            limit = limit
            )
    FigureName = f'seasonal_{parameter}'
     
    fig.savefig(
          b.LATEX(FigureName, folder = 'distributions/en/'),
          dpi = 400
          )
    
    
# main()
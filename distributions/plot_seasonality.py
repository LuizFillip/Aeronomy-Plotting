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
        wspace = 0.2
        )
    
    return fig, ax 



def plot_distributions_seasons(
        df, 
        parameter = 'gamma',
        solar_limit = 86, 
        translate = False,
        outliner = 10,
        limit = None
        ):
    
    fig, ax = FigureAxes()

    names = ['march', 'june', 'september', 'december']
    
    for row, name in enumerate(names):
        
        total_epb = []
        total_day = []
        
        df_season = c.SeasonsSplit(
            df, 
            name, 
            translate = translate
            )
        
        df_index = c.DisturbedLevels(df_season.sel_season)
        
        F107_labels = df_index.solar_labels(solar_limit)
        
        for index, df_level in enumerate(df_index.F107(solar_limit)):
    
            data, epb = pl.plot_distribution(
                    ax[row, 0], 
                    df_level, 
                    parameter,
                    label = F107_labels[index],
                    outliner = outliner, 
                    translate = translate,
                    limit = limit
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
            x = 0.55,
            translate = translate
            )
            
        
    pl.FigureLabels(
        fig, 
        translate = translate, 
        parameter = parameter,
        fontsize = 30
        )
    
    return fig


def main():
    
    translate = True
    parameter = 'gamma'
    df = c.load_results('saa')
    solar_limit = c.limits_on_parts(df['f107a'])
    
    fig = plot_distributions_seasons(
            df, 
            parameter = parameter,
            solar_level = solar_limit,
            translate = translate,
            outliner = 10,
            limit = False
            )
    
    FigureName = f'seasonal_{parameter}'
    
    if translate:
        folder = 'distributions/pt/'
    else:
        folder = 'distributions/en/'
        
    
    # fig.savefig(
    #     b.LATEX(FigureName, folder),
    #     dpi = 400
    #     )
    

    
# main()


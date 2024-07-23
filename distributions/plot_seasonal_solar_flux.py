import base as b 
import matplotlib.pyplot as plt 
import core as c
import plotting as pl 



b.config_labels(fontsize = 25, blue = True)

def plot_distributions_seasons(
        df, 
        parameter = 'gamma',
        solar_level = 86, 
        translate = False,
        outliner = 10,
        limit = None
        ):
    
    fig, ax = pl.axes_for_seasonal_plot()

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
        
        F107_labels = df_index.solar_labels(solar_level)
        
        for index, df_level in enumerate(df_index.F107(solar_level)):
    
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
            
            ax[row, 1].set(
                ylim = [0, 350], 
                yticks = list(range(0, 400, 100))
                )
                    
            ax[row, index].text(
                0.02, 0.82,
                f'{df_season.name}',
                transform = ax[row, index].transAxes
                )
            

        TOTAL = [total_epb, total_day]
       
        pl.plot_events_infos(
            ax, row, TOTAL, 
            x = 0.58,
            y = 0.3,
            parameter = parameter,
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
    
    translate = False
    parameter = 'gamma'
    df = c.load_results('saa', eyear = 2022)
    
    solar_limit = c.limits_on_parts(df['f107a'])
    
    fig = plot_distributions_seasons(
            df, 
            parameter = parameter,
            solar_level = solar_limit,
            translate = translate,
            outliner = 10,
            limit = True
            )
    
    FigureName = f'seasonal_{parameter}2'
    
    if translate:
        folder = 'distributions/pt/'
    else:
        folder = 'distributions/en/'
        
        
    # fig.savefig(
    #     b.LATEX(FigureName, folder),
    #     dpi = 400
    #     )
    

    plt.show()
main()


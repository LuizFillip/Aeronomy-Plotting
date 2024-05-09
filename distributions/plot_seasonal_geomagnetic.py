import matplotlib.pyplot as plt
import base as b
import core as c
import plotting as pl


b.config_labels(fontsize = 25)


        
def FigureAxes(nrows = 4):
    
    fig, ax = plt.subplots(
          ncols = nrows // 2, 
          nrows = nrows,
          figsize = (20, 14), 
          dpi = 300, 
          sharex = True, 
          sharey = 'col'
        )
    
    plt.subplots_adjust(
        hspace = 0.1, 
        wspace = 0.2
        )
    
    return fig, ax 

def plot_storm_levels_distribution(
        df, 
        parameter = 'gamma',
        level = -50, 
        translate = False,
        outliner = 10,
        limit =  True
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
        kp_labels = df_index.geomagnetic_labels(level)
        
        for index, df_level in enumerate(df_index.Dst(level)):
    
            data, epb = pl.plot_distribution(
                    ax[row, 0], 
                    df_level, 
                    parameter,
                    label = kp_labels[index],
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
                    label = kp_labels[index], 
                    # limit = limit
                    )
            
            total_day.append(days)
        
            ax[row, 1].set(
                ylim = [0, 350], 
                yticks = list(range(0, 400, 100))
                )
                    
            ax[row, index].text(
                0.35, 0.82,
                f'{df_season.name}',
                transform = ax[row, index].transAxes
                )
    
        LIST = [total_epb, total_day]
        pl.plot_events_infos(
            ax, row, LIST, 
            x = 0.58,
            y = 0.3,
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

    df = c.load_results('saa')
    parameter ='gamma'
    
    fig = plot_storm_levels_distribution(
        df, 
        parameter= parameter,
        level = -30, 
        translate = translate,
        limit =  True
        )
    
    if translate:
        folder = 'distributions/pt/'
    else:
        folder = 'distributions/en/'
        
    FigureName = f'geomagnetic_{parameter}'
    
    FigureName = 'geomagnetic_seasonal'
    
    fig.savefig(
        b.LATEX(FigureName, folder = folder),
        dpi = 400
        )
    
    
main()
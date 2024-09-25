import base as b
import core as c
import plotting as pl


b.config_labels(fontsize = 25, blue = True)


def plot_storm_levels_distribution(
        df, 
        parameter = 'gamma',
        level = -50, 
        translate = False,
        outliner = 10,
        limit =  True,
        random_state = None
        ):
    
    fig, ax = pl.axes_for_seasonal_plot()
    
    names = ['march', 'june', 'september', 'december']
    
    if random_state is not None:
        vmax = 150
        step = 50
    else:
        vmax = 400
        step = 100
        
    for row, name in enumerate(names):
        
        total_epb = []
        total_day = []
        
        df_season = c.SeasonsSplit(
            df, 
            name, 
            translate = translate
            )
        
        
        df_index = c.DisturbedLevels(df_season.sel_season)
        
        if level == 3:
            datasets = df_index.Kp(level, random_state)
            kp_labels = df_index.geomagnetic_labels(
                level, dst = False)
        else:
            kp_labels = df_index.geomagnetic_labels(
                level, dst = True)
            datasets = df_index.Dst(level, random_state)
       
        
        for index, df_level in enumerate(datasets):
            
            
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
                    )
            
            total_day.append(days)
        
            ax[row, 1].set(
                ylim = [0, 350], 
                yticks = list(range(0, vmax, step))
                )
                    
            ax[row, index].text(
                0.02, 0.82,
                f'{df_season.name}',
                transform = ax[row, index].transAxes
                )
    
        LIST = [total_epb, total_day]
        pl.plot_events_infos(
            ax, row, LIST, 
            x = 0.58,
            y = 0.3,
            translate = translate, 
            fontsize = 25
            )
            
        
    pl.FigureLabels(
        fig, 
        translate = translate, 
        parameter = parameter,
        fontsize = 35
        )
        
    return fig


def main():
    
    translate = True

    df = c.load_results('saa', eyear = 2022)
    parameter ='gamma'
    
    
    fig = plot_storm_levels_distribution(
        df, 
        parameter= parameter,
        level = -30, 
        translate = translate,
        limit = True, 
        outliner = 10, 
        random_state = None
        )
    
    if translate:
        folder = 'distributions/pt/'
    else:
        folder = 'distributions/en/'
        
    FigureName = 'geomagnetic_seasonal'
    
    fig.savefig(
        b.LATEX(FigureName, folder = folder),
        dpi = 400
        )
    
    
main()
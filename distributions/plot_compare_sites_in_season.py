import matplotlib.pyplot as plt
import core as c
import plotting as pl
import base as b 


b.config_labels(fontsize = 25)

def plot_compare_sites_in_season(
        parameter = 'gamma', 
        translate = True
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
            
            df_season = c.SeasonsSplit(df, name, translate = translate)
            
            label = f'({index + 1}) {titles[index]}'
        
            data, epb = pl.plot_distribution(
                    ax[row, 0], 
                    df_season.sel_season, 
                    parameter,
                    label = label,
                    drop_ones = True
                    )
            
            total_epb.append(epb)
            
            days = pl.plot_histogram(
                    ax[row, 1], 
                    data, 
                    index,
                    label = label
                    )
            total_day.append(days)
                    
            ax[row, index].text(
                0.07, 0.82, 
                f'{df_season.name}',
                transform = ax[row, index].transAxes
                )
            
            ax[row, index].set(ylim = [0, 400])
        
        LIST = [total_epb, total_day]
        
        pl.plot_events_infos(
            ax, row, 
            LIST, x = 0.55, 
            translate = translate
            )
        
    pl.FigureLabels(
            fig, 
            translate = translate, 
            fontsize = 30
            )
    plt.show()
    return fig

def main():
    
    fig = plot_compare_sites_in_season(
            parameter = 'gamma'
            )
    
    FigureName = 'compare_jic_saa_in_season'
      
    fig.savefig(
          b.LATEX(FigureName, 
                  folder = 'distributions/pt/'),
          dpi = 400
          )


# main()
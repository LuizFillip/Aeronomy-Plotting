import base as b 
import matplotlib.pyplot as plt 
import core as c
import plotting as pl 



b.config_labels(fontsize = 25, blue = True)

def plot_distributions_seasons(
        df, 
        parameter = 'gamma',
        translate = False,
        outliner = 10,
        limit = True
        ):
    
    fig, axs = plt.subplots(
          ncols = 1, 
          nrows = 4,
          figsize = (8, 14), 
          dpi = 300, 
          sharex = True, 
          sharey = True
        )
    
    plt.subplots_adjust(
        hspace = 0.1, 
        wspace = 0.05
        )

    names = ['march', 'june', 'september', 'december']
    
    for row, ax in enumerate(axs.flat):
        
        total_epb = []
        
        df_season = c.SeasonsSplit(
            df, 
            names[row], 
            translate = translate
            )
        
        df_index = c.DisturbedLevels(df_season.sel_season)
                
        kp_labels = df_index.geomagnetic_labels(-30, dst = True)
        
        datasets = df_index.Dst(-30, random_state = None)
        
        for index, df_level in enumerate(datasets):
    
            data, epb = pl.plot_distribution(
                    ax, 
                    df_level, 
                    parameter,
                    label = kp_labels[index],
                    outliner = outliner, 
                    translate = translate,
                    limit = limit
                    )
            
            total_epb.append(epb)
           
            ax.text(
                0.02, 0.82,
                f'{df_season.name}',
                transform = ax.transAxes
                )
            
        pl.plot_infos_in_distribution(
                ax, 
                total_epb, 
                x = 0.52, 
                y = 0.28,
                translate = True,
                offset_y = 0.12
                )
        
    axs[0].legend(
        ncol = 2, bbox_to_anchor = (0.5, 1.3), 
        loc = 'upper center')
    
    axs[-1].set(
        xlabel = b.y_label('gamma')
        )
    ylabel1 = "Probabilidade de ocorrência (\%)"
    
    fontsize = 30
    fig.text(
         -0.01, 0.3, 
         ylabel1, 
         fontsize = fontsize, 
         rotation = 'vertical'
         )
    
    return fig


def main():
    
    translate = True
    parameter = 'gamma'
    df = c.load_results('saa')
    
    fig = plot_distributions_seasons(
            df, 
            parameter = parameter,
            translate = translate,
            outliner = 10,
            limit = True
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
    

    plt.show()
# main()


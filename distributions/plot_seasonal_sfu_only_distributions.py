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
        
        F107_labels = df_index.solar_labels(solar_level)
        
        solar_flux_data = df_index.F107_2(solar_level)
        
        for index, df_level in enumerate(solar_flux_data):
    
            data, epb = pl.plot_distribution(
                    ax, 
                    df_level, 
                    parameter,
                    label = F107_labels[index],
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
                title = '$V_P$', 
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


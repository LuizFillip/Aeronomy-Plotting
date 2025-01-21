import base as b 
import matplotlib.pyplot as plt 
import core as c
import plotting as pl 



b.config_labels(fontsize = 30, blue = True)

def plot_distributions_seasons(
        df, 
        parameter = 'gamma',
        solar_level = 86, 
        translate = False,
        outliner = 10,
        limit = None
        ):
    
    fig, axs = plt.subplots(
          ncols = 2, 
          nrows = 2,
          figsize = (18, 12), 
          dpi = 300, 
          sharex = True, 
          sharey = True
        )
    
    plt.subplots_adjust(
        hspace = 0.05, 
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
            
            label = f'({index + 1}) {F107_labels[index]}'
            
            data, epb = pl.plot_distribution(
                    ax, 
                    df_level, 
                    parameter,
                    label = label,
                    outliner = outliner, 
                    translate = translate,
                    limit = limit
                    )
            
            total_epb.append(epb)
            
            l = b.chars()[row]
           
            ax.text(
                0.02, 0.89,
                f'({l}) {df_season.name}',
                transform = ax.transAxes
                )
            
            ax.set(ylim = [-10, 120])
            
        pl.plot_infos_in_distribution(
                ax, 
                total_epb, 
                x = 0.47, 
                y = 0.25,
                translate = translate,
                title = '$V_P$', 
                offset_y = 0.12
                )
        
    
    axs[0][0].legend(
        ncol = 2, 
        bbox_to_anchor = (1, 1.2), 
        loc = 'upper center'
        )
    
    if translate:
        prob_name = "Probabilidade de ocorrência (\%)"
    else:
        prob_name = "EPB occurrence probability (\%)"
        
        
    fontsize = 30
    fig.text(
         0.04, 0.25, 
         prob_name, 
         fontsize = fontsize  + 5, 
         rotation = 'vertical'
         )

    
    fig.text(
         0.45, 0.04, 
         "$\gamma_{RT} ~(10^{-3} ~s^{-1}) $", 
         fontsize = fontsize + 5, 
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
    
    FigureName = f'seasonal_{parameter}_en'
    
    if translate:
        folder = 'distributions/pt/'
    else:
        folder = 'distributions/en/'
        
        
    fig.savefig(
        b.LATEX(FigureName, 'posdoc'),
        dpi = 400
        )
    

    plt.show()
# main()

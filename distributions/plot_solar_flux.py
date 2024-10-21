import matplotlib.pyplot as plt
import base as b
import core as c 
import plotting as pl 
 

b.config_labels(fontsize = 30, blue = True)

legend_args = dict(
    ncol = 3, 
    loc = 'upper center', 
    labelcolor = 'linecolor',
    columnspacing = 0.2,
    )


        
def plot_distributions_solar_flux(
        df, 
        parameter = 'gamma',
        level = 86, 
        translate = False,
        outliner = 10,
        limit = None, 
        fontsize = 30
        ):
    
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 2,
        sharex = True,
        figsize = (14, 14)
        )
    
    plt.subplots_adjust(hspace = 0.05)
        
    df_index = c.DisturbedLevels(df)
    
    F107_labels = df_index.solar_labels(level)
     
    total_epb = []
    total_day = []
   
    for i, ds in enumerate(df_index.F107_2(level)):
        
        index = i + 1
        label = f'({index}) {F107_labels[i]}'
    
        data, epbs = pl.plot_distribution(
                ax[0], 
                ds,
                parameter = parameter,
                label = label,
                axis_label = True,
                outliner = outliner, 
                translate = translate,
                limit = limit
            )
        days = pl.plot_histogram(
                ax[1], 
                data, 
                i, 
                label, 
                parameter = parameter,
                axis_label = True,
                translate = translate, 
              
            )
        
        ax[1].set(ylim = [0, 600])
        ax[0].set(xlabel = '')
        total_epb.append(epbs)
        total_day.append(days)
        
        l = b.chars()[i]
        
        ax[i].text(
            0.03, 0.87,
            f'({l})',
            transform = ax[i].transAxes, 
            fontsize = fontsize + 5
            
            )
        
    x = 0.67
    y = 0.25
    offset_y = 0.1
    
    ax[1].legend(**legend_args, fontsize = fontsize)
    ax[0].legend(**legend_args, fontsize = fontsize)
    
    pl.plot_infos_in_distribution(
        ax[0], 
        x = x, 
        y = y, 
        translate = translate, 
        values = total_epb, 
        offset_y = offset_y, 
        fontsize = fontsize
        )
    
    pl.plot_infos_in_distribution(
        ax[1], 
        x = x,
        y = y,
        values = total_day, 
        title = parameter, 
        translate = translate, 
        offset_y = offset_y, 
        fontsize = fontsize
        )
    
    return fig



def main():
    
    translate = True

    df = c.load_results('saa', eyear = 2022)

    limit = c.limits_on_parts(df['f107a'], parts = 2 )

    parameter = 'gamma2'
    
    fig = plot_distributions_solar_flux(
            df, 
            parameter,
            level = limit, 
            translate = translate, 
            outliner = 10,
            limit = True
            )
    
    if translate:
        folder = 'distributions/pt/'
    else:
        folder = 'distributions/en/'
    
    if parameter == 'gamma2':
        FigureName = f'solar_flux_{parameter}_without_vp'
    else:
        FigureName = f'solar_flux_{parameter}'
    
    fig.savefig(
        b.LATEX(FigureName, folder),
        dpi = 400
        )


    plt.show()
    
# main()


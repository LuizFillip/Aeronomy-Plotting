import matplotlib.pyplot as plt
import base as b
import core as c 
import plotting as pl 

b.config_labels(fontsize = 25)

legend_args = dict(
    ncol = 2, 
    loc = 'upper center', 
    labelcolor = 'linecolor'
    
    )

def plot_compare_sites_in_solar_flux(
        year = 2018,
        parameter = 'gamma', 
        translate = True,
        outliner = 10
        ):
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 2,
        sharex = True,
        figsize = (12, 12)
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    titles = ['São Luís', 'Jicamarca']
    
    total_epb = []
    total_day = []
    
    for i, ds in enumerate(c.get_same_length(year)):
        index = i + 1
        label = f'({index}) {titles[i]}'
        
        
        data, epbs = pl.plot_distribution(
                ax[0], 
                ds,
                parameter,
                label = label,
                axis_label = True,
                outliner = outliner, 
                translate = True, 
                limit = 1.6
            )
        
        days = pl.plot_histogram(
                ax[1], 
                data, 
                i, 
                label, 
                parameter = parameter,
                axis_label = True,
                translate = translate
            )
        
        total_epb.append(epbs)
        total_day.append(days)
        
        ax[1].set(ylim = [0, 200])
        ax[0].set(xlabel = '')
        
        
    x = 0.7
    y = 0.25
    offset_y = 0.1
    
    ax[1].legend(**legend_args)
    ax[0].legend(**legend_args)
    
    pl.plot_infos(
        ax[0], 
        x = x, 
        y = y, 
        translate = translate, 
        values = total_epb, 
        offset_y = offset_y
        )
    
    pl.plot_infos(
        ax[1], 
        x = x,
        y = y,
        values = total_day, 
        epb_title = False, 
        translate = translate, 
        offset_y = offset_y
        )
    
    return fig 

def main():
    
    
    FigureName = 'compare_jic_saa'
      
    translate = True

    parameter ='gamma'
    year = 2015
    fig = plot_compare_sites_in_solar_flux(
        year,
        parameter = parameter, 
        translate = translate,
        outliner = 0
        )
    
    if translate:
        folder = 'distributions/pt/'
    else:
        folder = 'distributions/en/'
        
    FigureName = f'longitudinal_{parameter}'
        
    # fig.savefig(
        # b.LATEX(FigureName, folder = folder),
        # dpi = 400
        # )
    
    
    
# main()


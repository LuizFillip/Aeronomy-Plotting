import matplotlib.pyplot as plt
import base as b
import core as c 
import plotting as pl 

b.config_labels(fontsize = 25)

def plot_compare_sites_in_solar_flux(
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
    
    for i, ds in enumerate(c.get_same_length(2015)):
        index = i + 1
        label = f'({index}) {titles[i]}'
        
        
        data, epbs = pl.plot_distribution(
                ax[0], 
                ds,
                parameter,
                label = label,
                axis_label = True,
                outliner = outliner, 
                translate = True
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
        
        ax[1].set(ylim = [0, 600])
        ax[0].set(xlabel = '')
        
        
    ax[0].legend(loc = 'upper center', ncol = 2)
    ax[1].legend(loc = 'upper center', ncol = 2)
    
    x = 0.68
    pl.plot_infos(ax[0], total_epb, 
                  x = x, 
                  translate = True)
    pl.plot_infos(ax[1], total_day, 
                  x = x, 
                  epb_title = False, 
                  translate = True)

    b.plot_letters(ax, y = 0.87, x = 0.02)
    
    return fig 

def main():
    
    fig = plot_compare_sites_in_solar_flux()
    
    FigureName = 'compare_jic_saa'
      
    # fig.savefig(
    #       b.LATEX(FigureName, 
    #               folder = 'distributions/pt/'),
    #       dpi = 400
    #       )
    # 
# main()

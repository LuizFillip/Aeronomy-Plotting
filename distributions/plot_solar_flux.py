import matplotlib.pyplot as plt
import base as b
import core as c 
import plotting as pl 
 

b.config_labels(fontsize = 25)


        
def plot_distributions_solar_flux(
        df, 
        parameter = 'gamma',
        level = 86, 
        translate = False,
        outliner = 10,
        limit = None
        ):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 2,
        sharex = True,
        figsize = (12, 12)
        )
    
    plt.subplots_adjust(hspace = 0.05)
        
    df_index = c.DisturbedLevels(df)
    
    F107_labels = df_index.solar_labels(level)
     
    total_epb = []
    total_day = []
    
    for i, ds in enumerate(df_index.F107(level)):
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
                index, 
                label, 
                parameter = parameter,
                axis_label = True,
                translate = translate
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
            fontsize = 30
            )
        
    x = 0.7
    y = 0.17
    
    ax[1].legend(ncol = 2, loc = 'upper center')
    ax[0].legend(ncol = 2, loc = 'upper center')
    
    pl.plot_infos(
        ax[0], 
        x = x, 
        y = y, 
        translate = translate, 
        values = total_epb
        )
    
    pl.plot_infos(
        ax[1], 
        x = x , #+ 0.05
        y = y,
        values = total_day, 
        epb_title = False, 
        translate = translate
        )
    
    # print(sum(total_epb))
    return fig



def main():
    
    translate = False
    df = c.load_results('saa', eyear = 2022)
    #print(df['epb'].sum())
    limit = c.limits_on_parts(df['f107a'], parts = 2 )

    parameter = 'gamma'
    
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
        
    FigureName = f'solar_flux_{parameter}2'
    
    fig.savefig(
        b.LATEX(FigureName, folder),
        dpi = 400
        )



main()


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

def plot_epbs_number(ax, data, color = 'k'):
    if color == 'k':
        offset = -12
        
    else:
        offset = 5
    for x, y, z in data[['start', 'rate', 'epbs']].values:
        
        ax.text(x - 0.05, (y *100) + offset, 
                int(z),
                transform = ax.transData, 
                color = color)
        
def plot_distributions_geomagnetic(
        df, 
        parameter = 'gamma',
        level = -50, 
        translate = False,
        outliner = 5,
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

    kp_labels = df_index.geomagnetic_labels(level)
    total_epb = []
    total_day = []
   
    
    for i, ds in enumerate(df_index.Dst(level)):
        
        index = i + 1
        label = f'({index}) {kp_labels[i]}'
    
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
        
        # plot_epbs_number(ax[0], data, color = colors[i])
                        
        days = pl.plot_histogram(
                ax[1], 
                data, 
                i, 
                label, 
                parameter = parameter,
                axis_label = True,
                translate = translate
            )
        
        ax[1].set(ylim = [0, 600])
        ax[0].set(xlabel = '')
        total_epb.append(epbs)
        total_day.append(days)
        
        if i < 2:
            l = b.chars()[i]
            
            ax[i].text(
                0.03, 0.87,
                f'({l})',
                transform = ax[i].transAxes, 
                fontsize = 30
                )
            
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
        x = x, #
        y = y,
        values = total_day, 
        epb_title = False, 
        translate = translate, 
        offset_y = offset_y 
        )
    
    return fig



def main():
    
    translate = True
    df = c.load_results('saa', eyear = 2022)
    parameter = 'gamma'
    
    fig = plot_distributions_geomagnetic(
            df, 
            parameter,
            level = -30, 
            translate = translate, 
            outliner = 10,
            limit = True
            )
    
    if translate:
        folder = 'distributions/pt/'
    else:
        folder = 'distributions/en/'
        
    FigureName = f'geomagnetic_{parameter}'
    
    # infile = 'G:\\My Drive\\LaTex\\docs\\img\\distributions\\pt\\'
    fig.savefig(
        folder,  FigureName,
        dpi = 400
        )


    plt.show()
    
main()


import matplotlib.pyplot as plt
import base as b
import core as c 
import plotting as pl 
 

b.config_labels(fontsize = 25)


def plot_distributions_solar_flux(
        df, 
        col = 'gamma',
        level = 86
        ):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 2,
        sharex = True,
        figsize = (12, 12)
        )
    
    plt.subplots_adjust(hspace = 0.05)
        
    labels = [
        '$F_{10.7} < $' + f' {level}',
        '$F_{10.7} > $' + f' {level}'
        ]
    
  
    solar_dfs = c.solar_levels(
        df, 
        level,
        flux_col = 'f107a'
        )
     
    total_epb = []
    total_day = []
    
    for i, ds in enumerate(solar_dfs):
        index = i + 1
        label = f'({index}) {labels[i]}'
    
        epbs = pl.plot_distribution(
                ax[0], 
                ds,
                col = col,
                label = label,
                axis_label = True
            )
        
        days = pl.plot_histogram(
                ax[1], 
                ds, 
                index, 
                label, 
                col = col,
                axis_label = True
            )
        
        ax[1].set(ylim = [0, 500])
        ax[0].set(xlabel = '')
        total_epb.append(epbs)
        total_day.append(days)
        
        l = b.chars()[i]
        
        ax[i].text(
            0.02, 0.85,
            f'({l})',
            transform = ax[i].transAxes
            )
        
    # print('days', sum(total_day))
    # print('epbs', sum(total_epb))
    
    ax[1].legend(ncol = 2, loc = 'upper center')
    ax[0].legend(ncol = 2, loc = 'upper center')
    
    pl.plot_infos(ax[0], total_epb)
    pl.plot_infos(ax[1], total_day,
                title = '$\gamma_{RT}$ total')
    
    return fig

    


def save_figures(df):
    
    for col in ['gamma', 'vp', 'gravity']:

        FigureName = f'PD_{col}_effects'
        
        fig = plot_distributions_solar_flux(
                df, 
                col,
                level = 83.66
                )
        
        fig.savefig(
            b.LATEX(FigureName),
            dpi = 400
            )

df = c.concat_results('saa')

def main(df, col = 'gamma'):
    
    
    fig = plot_distributions_solar_flux(
            df, 
            col,
            level = 83.66
            )
    
    FigureName = f'PD_{col}_effects'
    
    # fig.savefig(
    #     b.LATEX(FigureName),
    #     dpi = 400
    #     )

# save_figures(df)


# main(df)
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
        figsize = (12, 10)
        )
    
    plt.subplots_adjust(hspace = 0.1)
        
    labels = [
        '$F_{10.7} < $' + f' {level}',
        '$F_{10.7} > $' + f' {level}'
        ]
    
  
    solar_dfs =  c.solar_levels(
        df, 
        level,
        flux_col = 'f107a'
        )
     
    total_epb = []
    total_day = []
    
    for i, ds in enumerate(solar_dfs):
        index = i + 1
        name = f'({index}) {labels[i]}'
    
        epbs = pl.plot_distribution(
                ax[1], 
                ds,
                col = col,
                label = name
            )
        
        days = pl.plot_histogram(ax[0], ds, i, name)
        
        total_epb.append(pl.fmt(index, epbs))
        total_day.append(pl.fmt(index, days))
          
    ax[1].legend(ncol = 2,  loc = 'upper center')
    
    pl.plot_infos(ax[1], total_epb)
    pl.plot_infos(ax[0], total_day,
               title = '$\gamma_{RT}$ total')
    
    return fig

    
df = c.concat_results('saa')

col = 'gamma'

# fig = plot_distributions_solar_flux(
#         df, 
#         col,
#         level = 86
#         )

df = df.dropna()


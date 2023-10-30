import events as ev 
import base as b 
import matplotlib.pyplot as plt


def plot_count_epbs_occurrences(df, level):
    
    solar_dfs =  ev.solar_levels(
        df, 
        level,
        flux_col = 'f107a'
        )
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 2,
        sharex = True,
        figsize = (12, 8)
        )
            
    plt.subplots_adjust(hspace = 0.1)
    
    names = [
        '$F_{10.7} < $' + f' {level}',
        '$F_{10.7} > $' + f' {level}'
        ]
    
    for i, ds in enumerate(solar_dfs):
    
        dataset = ev.monthly_occurences(ds)
        
        dataset.plot(
            kind = 'bar',
            ax = ax[i], 
            color =  ['k', 'gray'],
            stacked = True, 
            legend = False
            )
    
        ax[i].set(
            ylim = [0, 200],
            ylabel = 'Number of nights',
            xlabel = 'Months',
            xticklabels = b.number_to_months()
            )
        
        epb_count = dataset['epb'].sum()
        
        l = b.chars()[i]
        n = names[i]
        info = f'({l}) {n} ({epb_count} EPBs events)'
        
        ax[i].text(
            0.02, 0.85, info, 
            transform = ax[i].transAxes
            )
        
    plt.xticks(rotation = 0)
    
    ax[0].legend(
        ['With EPB', 'Without EPB'], 
        ncol = 2, 
        loc = 'upper center', 
        bbox_to_anchor = (0.5, 1.2)
        )
    return fig 


df = ev.concat_results('saa')

 
level = 86

fig = plot_count_epbs_occurrences(df, level)

# fig.savefig(b.LATEX('seasonal_variation'), dpi = 400)

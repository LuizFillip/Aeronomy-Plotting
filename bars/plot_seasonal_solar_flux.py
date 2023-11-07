import events as ev 
import base as b 
import matplotlib.pyplot as plt


def plot_count_epbs_occurrences(df, parts = 2):
    
    limits = ev.limits_on_parts(df['f107a'], parts)
    
    solar_dfs =  ev.solar_levels(
        df, 
        limits,
        flux_col = 'f107a'
        )
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = parts,
        sharex = True,
        figsize = (12, 6 + parts)
        )
            
    plt.subplots_adjust(hspace = 0.1)
    
    if len(limits) == 1:
    
        names = [
            '$F_{10.7} < $' + f' {limits[0]}',
            '$F_{10.7} > $' + f' {limits[0]}'
            ]
        
    else:
        names = [
            '$F_{10.7} < $' + f' {limits[0]}',
            f' {limits[0]}' + '$< F_{10.7} < $' +  f' {limits[1]}',
            '$F_{10.7} > $' + f' {limits[1]}'
            ]
        
    
    for i, ds in enumerate(solar_dfs):
    
        dataset = ev.monthly_occurrences(ds)
        
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
            0.02, 0.85, 
            info, 
            transform = ax[i].transAxes
            )
        
    plt.xticks(rotation = 0)
    
    ax[0].legend(
        ['With EPB', 'Without EPB'], 
        ncol = 2, 
        loc = 'upper center', 
        bbox_to_anchor = (0.5, 1.3)
        )
    return fig 


df = ev.concat_results('saa')

    
fig = plot_count_epbs_occurrences(df, parts = 3)

# fig.savefig(b.LATEX('solar_seasonal_variation'))
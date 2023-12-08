import matplotlib.pyplot as plt 
import base as b
import events as ev 

path = 'database/epbs/events_types.txt'

b.config_labels(fontsize = 28)

args = dict(
    edgecolor = 'black', 
    color = 'gray', 
    linewidth = 1
    )

def plot_epbs_with_indices(
        df,
        solar_level = 86,
        kp_level = 3
        ):
    
    fig, ax = plt.subplots(
        nrows = 3, 
        dpi = 300, 
        figsize = (14, 11)
        )
    
    plt.subplots_adjust(hspace = 0.1)
        
    ds = ev.yearly_occurrences(df)
    
    ds.plot(
        kind = 'bar', 
        ax = ax[2], 
        legend = False,
        color =  ['k', 'gray'],
        stacked = True, 
        )
     
    ax[0].plot(df['f107'])
        
    ax[0].plot(df['f107a'], lw = 2)
    
    ax[1].bar(df.index, df['kp'], width = 1)
    
    ax[2].legend(
        ['With EPB', 'Without EPB'], 
        ncol = 2, 
        loc = 'upper center', 
        # bbox_to_anchor = (0.5, 1.2)
        )
    
    ax[0].set(
        xlim = [df.index[0], df.index[-1]],
        ylabel = '$F_{10.7}$ (sfu)', 
        yticks = list(range(50, 300, 50))
        )
    
    ax[1].set(
        xlim = [df.index[0], df.index[-1]],
        ylabel = 'Kp index', 
        yticks = list(range(0, 12, 3)),
        ylim = [0, 10]
        )
    
    ax[2].set(
        ylabel = 'Number of nights',
        xlabel = 'Years', 
        # yticks = list(range(0, 500, 100)), 
        ylim = [0, 700]
        )
    
    ax[0].axhline(solar_level, color = 'r', lw = 2)
    
    ax[1].axhline(kp_level, color = 'r', lw = 2)
    
    fig.autofmt_xdate(
        rotation = 0, 
        ha = 'center')

    for i, ax in enumerate(ax.flat):
       
       l = b.chars()[i]
       ax.text(
           0.02, 0.83, f'({l})', 
           transform = ax.transAxes
           )
    
    return fig

# df = ev.concat_results('saa')
# df = ev.epbs(geo = True)
# fig = plot_epbs_with_indices(df)

# fig.savefig(b.LATEX('annual_variation'))
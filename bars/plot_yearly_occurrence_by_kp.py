import matplotlib.pyplot as plt 
import base as b
import events as ev 

path = 'database/epbs/events_types.txt'

b.config_labels()

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
        nrows = 2, 
        dpi = 300, 
        figsize = (12, 8)
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    levels = ev.kp_levels(
            df, 
            level = 3, 
            kp_col = 'kp'
            )
    names = [f'$Kp \\leq$ {kp_level}', 
              f'$Kp >$ {kp_level}']
    
    for i, ds in enumerate(levels):
        
        dataset = ev.yearly_occcurrences(ds)
        
        dataset.plot(
            kind = 'bar', 
            ax = ax[i], 
            legend = False,
            color =  ['k', 'gray'],
            stacked = True, 
            )
        
        ax[i].set(
            ylabel = 'Number of nights',
            xlabel = 'Years', 
            yticks = list(range(0, 400, 100))
            )

        
        epb_count = dataset['epb'].sum()
        
        l = b.chars()[i]
        n = names[i]
        info = f'({l}) {n} ({epb_count} EPBs events)'
        
        ax[i].text(
            0.02, 0.83, info, 
            transform = ax[i].transAxes
            )
         
   
    ax[0].legend(
        ['With EPB', 'Without EPB'], 
        ncol = 2, 
        bbox_to_anchor = (0.5, 1.2),
        loc = 'upper center'
        )
    

    fig.autofmt_xdate(
        rotation = 0, ha = 'center')

    
    return fig

df = ev.concat_results('saa')
fig = plot_epbs_with_indices(df)

fig.savefig(b.LATEX('Kp_annual_variation'))
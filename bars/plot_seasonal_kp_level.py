import matplotlib.pyplot as plt 
import base as b
import core as c

b.config_labels()

def plot_seasonal_kp_level(
        df,
        solar_level = 86,
        kp_level = 3
        ):
    
    fig, ax = plt.subplots(
        nrows = 2, 
        dpi = 300, 
        sharex = True,
        figsize = (12, 8)
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    levels = c.kp_levels(
            df, 
            level =  kp_level, 
            kp_col = 'kp'
            )
    
    
    names = [
        f'$Kp \\leq$ {kp_level}', 
        f'$Kp >$ {kp_level}'
        ]
    
    for i, ds in enumerate(levels):
        
        dataset = c.month_occurrence(ds)
        
        dataset.plot(
            kind = 'bar',
            ax = ax[i], 
            color =  'gray',
            legend = False,
            edgecolor = 'k'
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
    
    
    return fig

df = c.concat_results('saa')
fig = plot_seasonal_kp_level(df)

# fig.savefig(b.LATEX('Kp_seasonal_variation'))
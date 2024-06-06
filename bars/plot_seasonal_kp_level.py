import matplotlib.pyplot as plt 
import base as b
import core as c
import PlasmaBubbles as pb 


b.config_labels()

def plot_seasonal_kp_level(
        df,
        kp_level = 3
        ):
    
    fig, ax = plt.subplots(
        nrows = 2, 
        dpi = 300, 
        sharex = True,
        figsize = (12, 8)
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    levels = c.DisturbedLevels(df).Kp(level = kp_level)

    names = [
        f'$Kp \\leq$ {kp_level}', 
        f'$Kp >$ {kp_level}'
        ]
    
    for i, ds in enumerate(levels):
        
        dataset = c.count_occurences(ds).month
        
        dataset.plot(
            kind = 'bar',
            ax = ax[i], 
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

df = b.load('events_class2')
ds = pb.sel_typing(df, typing = 'midnight')


fig = plot_seasonal_kp_level(ds)

# fig.savefig(b.LATEX('Kp_seasonal_variation'))



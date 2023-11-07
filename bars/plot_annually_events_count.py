import PlasmaBubbles as pb 
import matplotlib.pyplot as plt
import base as b 


b.config_labels()

def plot_annually_events_count(ds):
    
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 2,
        sharex = True,
        figsize = (12, 8)
        )

    period = ['sunset', 'midnight']
    
    plt.subplots_adjust(hspace = 0.1)
    
    ylims = [350, 40]
    
    for i, value in enumerate([1, 3]):
        
        df =  pb.year_occurrence(
            ds, value
            )
        
        total = int(df.values.sum())
    
        df.plot(
            kind = 'bar', 
            ax = ax[i], 
            legend = False
            )
        
        title = f'({b.chars()[i]}) Post {period[i]} '
        events = f'({total}  events)'
        
        plt.xticks(rotation = 0)
        
        ax[i].text(
            0.03, 0.85, 
            title + events, 
            transform = ax[i].transAxes
            )
        
        ax[i].set(
            ylabel = 'Nigths with EPB',
            ylim = [0, ylims[i]]
            )
        
   
    ax[0].legend(
        [f'{c}°' for c in ds.columns],
        ncol = 5, 
        title = 'Longitudinal sectors (2013 - 2022, $Kp > 3$)',
        bbox_to_anchor = (.5, 1.4), 
        loc = "upper center", 
        columnspacing = 0.6
        )
    
    ax[1].set(xlabel = 'Years')

path = 'database/epbs/events_types.txt'

 



# plot_annually_events_count(ds)
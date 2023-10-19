import PlasmaBubbles as pb 
import matplotlib.pyplot as plt
import base as b 


args = dict(facecolor = 'lightgrey', 
             edgecolor = 'black', 
             width = 0.9,
             color = 'gray', 
             linewidth = 1)

def plot_seasonal_occurrence(ds):
    
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 1,
        sharex = True,
        figsize = (12, 5)
        )
            
    df =  pb.month_occurrence(ds, 1)
    
    df['-50'].plot(
        kind = 'bar', 
        ax = ax, 
        legend = False, **args
        )

    
    plt.xticks(rotation = 0)
    
    ax.set(
        ylabel = 'Number of nights',
        xlabel = 'Months',
        xticklabels = b.number_to_months()
        )
        
    t = df['-50'].sum()
    
    ax.text(0.03, 0.85, f'{t} events', transform = ax.transAxes)
    
    ax.set(title = 'Post-sunset EPBs events (2013 - 2022)')
    
    return fig
    

# path = 'database/epbs/events_types.txt'

# ds = b.load(path)

# fig = plot_seasonal_occurrence(ds)

# fig.savefig(b.LATEX + 'Paper1//seasonal_variation', dpi = 300)
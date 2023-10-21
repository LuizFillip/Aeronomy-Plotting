import matplotlib.pyplot as plt 
import base as b
from geophysical_indices import INDEX_PATH
import PlasmaBubbles as pb 

path = 'database/epbs/events_types.txt'

b.config_labels()

args = dict(facecolor = 'lightgrey', 
             edgecolor = 'black', 
             width = 0.9,
             color = 'gray', 
             linewidth = 1)

def plot_epbs_by_solar_cycle():
    

    fig, ax = plt.subplots(
        nrows = 2, 
        dpi = 300, 
        figsize = (12, 8)
        )
    
    plt.subplots_adjust(hspace = 0.1)
     
    ep = b.load(path)
    
    yep = pb.year_occurrence(ep, 1)['-50']
    
    yep.plot(
        kind = 'bar', 
        ax = ax[0], 
        legend = False, **args
        )
 
    
    ax[0].set(
        ylabel = 'Nigths with EPB', 
        title = 'Annually EPBs occcurrence', 
        ylim = [0, 300]
        )
    
    
    ds = b.load(INDEX_PATH)
    
    ds = b.sel_dates(ds, ep.index[0], ep.index[-1])
    
    ax[1].plot(ds['f107'])
    ax[1].plot(ds['f107a'], lw = 2)
    
    
    ax[1].set(
        xlim = [ds.index[0], ds.index[-1]],
        xlabel = 'Years', 
        ylabel = '$F_{10.7}$ (sfu)'
        )
    
    
    ax[1].axhline(100, color = 'r', lw = 2)
    
    
    fig.autofmt_xdate(rotation=0)

    for i, ax in enumerate(ax.flat):
       
       l = b.chars()[i]
       ax.text(
           0.02, 0.8, f'({l})', 
           transform = ax.transAxes
           )
    
    return fig


fig = plot_epbs_by_solar_cycle()

# fig.savefig(b.LATEX + 'paper1/annual_variation')
import matplotlib.pyplot as plt 
import base as b
from geophysical_indices import INDEX_DY
import PlasmaBubbles as pb 

path = 'database/epbs/events_types.txt'

b.config_labels()

args = dict(
   facecolor = 'lightgrey', 
    edgecolor = 'black', 
    width = 0.9,
    color = 'gray', 
    linewidth = 1
    )

def plot_epbs_with_indices():
    

    fig, ax = plt.subplots(
        nrows = 3, 
        dpi = 300, 
        figsize = (12, 10)
        )
    
    plt.subplots_adjust(hspace = 0.1)
     
    ep = b.load(path)
    
    yep = pb.year_occurrence(ep, 1)['-50']
    
    yep.plot(
        kind = 'bar', 
        ax = ax[2], 
        legend = False, **args
        )
 
    
    ax[2].set(
        ylabel = 'Nigths with EPB',
        ylim = [0, 350],
        yticks = list(range(0, 350, 100))
        )
    
    
    ds = b.load(INDEX_DY)
    
    ds = b.sel_dates(ds, ep.index[0], ep.index[-1])
    
    ax[0].plot(ds['f107'])
        
    ax[0].plot(ds['f107a'], lw = 2)
    
    ax[1].bar(ds.index, ds['kp'], width = 1)
    
    
    ax[0].set(
        xlim = [ds.index[0], ds.index[-1]],
        ylabel = '$F_{10.7}$ (sfu)', 
        yticks = list(range(50, 300, 50))
        )
    
    ax[1].set(
        xlim = [ds.index[0], ds.index[-1]],
        ylabel = 'Kp index', 
        xlabel = 'Years', 
        yticks = list(range(0, 9, 2)),
        ylim = [0, 9]
        )
    
    
    ax[0].axhline(100, color = 'r', lw = 2)
    
    ax[1].axhline(3, color = 'r', lw = 2)
    

    fig.autofmt_xdate(rotation=0)

    for i, ax in enumerate(ax.flat):
       
       l = b.chars()[i]
       ax.text(
           0.02, 0.83, f'({l})', 
           transform = ax.transAxes
           )
    
    return fig


fig = plot_epbs_with_indices()

fig.savefig(b.LATEX('annual_variation'))
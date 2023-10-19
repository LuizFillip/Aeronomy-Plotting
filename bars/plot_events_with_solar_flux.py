import matplotlib.pyplot as plt 
import base as b
from geophysical_indices import INDEX_PATH
import PlasmaBubbles as pb 

path = 'database/epbs/events_types.txt'

b.config_labels()

def plot_epbs_by_solar_cycle():
    

    fig, ax = plt.subplots(
        nrows = 2, 
        dpi = 300, 
        figsize = (12, 8)
        )
    
    plt.subplots_adjust(hspace = 0.1)
     
    df = b.load(path)
    
    pb.year_occurrence(df, 1)['-50'].plot(
        kind = 'bar', 
        ax = ax[0], 
        legend = False
        )
    
    ds = b.load(INDEX_PATH)
    
    ds = b.sel_dates(ds, df.index[0], df.index[-1])
    
    ax[1].plot(ds['f107'])
    ax[1].plot(ds['f107a'], lw = 2)
    
    ax[0].set(
        ylabel = 'Nigths with EPB', 
        title = 'Annually EPBs occcurrence'
        )
    
    ax[1].set(xlabel = 'Years', ylabel = '$F_{10.7}$ sfu')
    ax[1].axhline(100, color = 'r', lw = 2)
    fig.autofmt_xdate(rotation=0)

    # ax[0].legend(
    #     ['EPB events occurrence'],
    #     ncols = 5, 
    #     bbox_to_anchor = (.5, 1.5), 
    #     loc = "upper center"
    #     )
    
    return fig


# fig = plot_epbs_by_solar_cycle()

# fig.savefig(b.LATEX + 'paper1/annual_variation')
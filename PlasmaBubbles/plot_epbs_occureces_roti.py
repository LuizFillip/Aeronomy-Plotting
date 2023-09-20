import datetime as dt
import base as b 
import matplotlib.pyplot as plt
import PlasmaBubbles as pb 


INDEX_PATH = 'database/indices/omni.txt'


args = dict(
    marker = 'o', 
    markersize = 3,
    linestyle = 'none'
    )



b.config_labels()

def get_infos(dn):
    df = b.load(INDEX_PATH)

    match = df.index.date == dn.date()
    
    res = df.loc[match, 
           ['f107a', 'kp', 'dst']
           ]
    
    out = []
    for c in res.columns:
        
        item = round(res[c].item(), 2)
        out.append(f'{c} = {item}')
    
    return '\n'.join(out)


def plot_epbs_occurrences_roti(
        ds
        ):

    fig, ax = plt.subplots(
        nrows = 2, 
        dpi = 300, 
        sharex = True, 
        figsize = (10, 6)
        )
    
    ds = ds[['-60', '-50', '-40']]
    
    plt.subplots_adjust(hspace = 0.1)
    
    color = ['k', 'b', 'r']
    dn = ds.index[0]
    
    for i, col in enumerate(ds.columns):
        
        the = pb.threshold(dn, int(col))
        
        line, = ax[0].plot(
            ds[col], 
            label = f'{col}° ({the})', 
            color = color[i], 
            **args
            )
        
        
        ax[0].axhline(
            the, 
            color = line.get_color()
            )
        
    
        ax[1].plot(
             pb.get_events_series(ds[col]), 
             marker = 'o',
             markersize = 3,
             color = line.get_color(), 
             label = f'{col}° ({the})'
            )
    

    ax[0].set(
        ylim = [0, 4], 
        yticks = list(range(5)),
        ylabel = 'ROTI (TECU/min)'
        )
    
    ax[1].legend(
        ncol = 5, 
        title = 'Longitudinal zones and thresholds (TECU/min)',
        bbox_to_anchor = (.5, 2.6), 
        loc = "upper center"
        )
    
   
    ax[1].set(
        ylabel = 'EPBs occurrence', 
        yticks = [0, 1], 
        ylim = [-0.2, 1.2]
        )
     
    b.format_time_axes(ax[1])
    
    ax[1].text(
        0.77, 
        0.48, 
        get_infos(dn), 
        transform = ax[1].transAxes
        )
    
    
    for limit in [0, 1]:
        ax[1].axhline(
            limit, 
            color = 'k', 
            linestyle = '--'
            )
    
    return fig


def single_plot(year = 2019):
    
    infile = f'database/EPBs/longs/{year}.txt'
    dn = dt.datetime(year, 2, 10, 21)
         
    ds = b.sel_times(
        b.load(infile), 
        dn, 
        hours = 9
        )
    
   
    plot_epbs_occurrences_roti(ds)
    
    return pb.get_all_events(ds)

# ds = single_plot(year = 2013)



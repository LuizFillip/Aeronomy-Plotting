import datetime as dt
import base as b 
import matplotlib.pyplot as plt
import PlasmaBubbles as pb 
import os
from geophysical_indices import INDEX_PATH


args = dict(
    marker = 'o', 
    markersize = 3,
    linestyle = 'none'
    )

b.config_labels()

def sel_indexes(
        dn, 
        idx = ['f107a', 'kp', 'dst']
        ):
    
    df = b.load(INDEX_PATH)

    match = df.index.date == dn.date()
    
    return df.loc[match, idx]

def get_infos(dn):
    
    res = sel_indexes(dn)
    
    out = []
    for c in res.columns:
        
        item = round(res[c].item(), 2)
        name = c.title()
        out.append(f'{name} = {item}')
    
    return '\n'.join(out)


def plot_epbs_occurrences_roti(
        ds,
        cols = None
        ):

    fig, ax = plt.subplots(
        nrows = 2, 
        dpi = 300, 
        sharex = True, 
        figsize = (14, 6)
        )
    
    # if cols is None:
        
    # cols = [5]
    ds = ds[[str(c * -10) for c in cols]]
    
    plt.subplots_adjust(hspace = 0.1)
    
    color = ['k', 'b', 
             'r', 'g', 
             'magenta']
    
    dn = ds.index[0]
    
    for i, col in enumerate(ds.columns):
        
        the = pb.threshold(dn, col)
        
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
        loc = "upper center", 
        columnspacing = 0.6
        )
    
   
    ax[1].set(
        ylabel = 'EPBs occurrence', 
        yticks = [0, 1], 
        xlim = [ds.index[0], 
                ds.index[-1]],
        ylim = [-0.2, 1.2]
        )
     
    b.format_time_axes(ax[1])
    
    ax[0].text(
        0.82, 
        0.53, 
        get_infos(dn), 
        transform = ax[0].transAxes
        )
    
    
    for limit in [0, 1]:
        ax[1].axhline(
            limit, 
            color = 'k', 
            linestyle = '--'
            )
    
    return fig


def single_plot(
        dn, 
        cols = [7, 6, 5, 4], 
        hours = 11
        ):
        
    infile = os.path.join(
            pb.PATH_LONG, 
            f'{dn.year}.txt'
        )
    
     
    ds = b.sel_times(
            b.load(infile),
            dn, 
            hours = hours
        )
    
    fig = plot_epbs_occurrences_roti(
            ds, 
            cols
        )
    
    return fig

dn = dt.datetime(2013, 1, 27, 21)

fig = single_plot(
        dn, 
        cols = [8, 7, 6, 5, 4], 
        hours = 11
        )
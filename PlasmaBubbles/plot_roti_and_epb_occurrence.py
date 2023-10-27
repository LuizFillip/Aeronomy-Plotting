import datetime as dt
import base as b 
import matplotlib.pyplot as plt
import PlasmaBubbles as pb 
from geophysical_indices import INDEX_DY2

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
    
    df = b.load(INDEX_DY2)

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
        factor,
        cols = None
        ):

    fig, ax = plt.subplots(
        nrows = 2, 
        dpi = 300, 
        sharex = True, 
        figsize = (11, 6)
        )
    
    ds = ds[[str(c * -10) for c in cols]]
    
    plt.subplots_adjust(hspace = 0.1)
    
    color = ['k', 'b', 
             'r', 'g', 
             'magenta']
    
    dn = ds.index[0]
    the = pb.threshold(dn, factor)
    
    title = f'Longitudinal zones (threshold = {the} TECU/min)'
    
    for i, col in enumerate(ds.columns):

        line, = ax[0].plot(
            ds[col], 
           # label = f'{col}°', 
            color = color[i], 
            **args
            )
        
        ax[0].axhline(
            the, 
            color = line.get_color(),
            label = f'Threshold = {the} TECU/min)'
            )
        
        ax[1].plot(
             pb.get_events_series(ds[col], factor), 
             marker = 'o',
             markersize = 3,
             color = line.get_color(), 
             label = f'{col}°'
            )
    

    ax[0].set(
        ylim = [0, 5], 
        yticks = list(range(6)),
        ylabel = 'ROTI (TECU/min)'
        )
    
    # ax[1].legend(
    #     ncol = 5, 
    #     title = title,
    #     bbox_to_anchor = (.5, 2.6), 
    #     loc = "upper center", 
    #     columnspacing = 0.6
    #     )
    
    ax[0].legend(loc = 'upper right')
   
    ax[1].set(
        ylabel = 'EPBs occurrence', 
        yticks = [0, 1], 
        xlim = [ds.index[0], 
                ds.index[-1]],
        ylim = [-0.2, 1.2]
        )
     
    b.format_time_axes(ax[1])
    
    # ax[0].text(
    #     0.78, 
    #     0.53, 
    #     get_infos(dn), 
    #     transform = ax[0].transAxes
    #     )
    
    
    for limit in [0, 1]:
        ax[1].axhline(
            limit, 
            color = 'k', 
            linestyle = '--'
            )
    
    return fig


def single_plot(
        dn, 
        cols = [8, 7, 6, 5, 4], 
        hours = 11, 
        factor = 8
        ):
        
    infile = pb.epb_path(dn.year, 'longs')
    
     
    ds = b.sel_times(
            b.load(infile),
            dn, 
            hours = hours
        )
    
    fig = plot_epbs_occurrences_roti(
            ds, 
            factor,
            cols = cols
        )
    
    plt.show()
    return fig

# dn = dt.datetime(2019, 1, 11, 20)

# fig = single_plot(
#         dn, 
#         hours = 11,
#         factor = 4
#         )


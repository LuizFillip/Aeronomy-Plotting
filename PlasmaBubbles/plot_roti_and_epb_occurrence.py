import datetime as dt
import base as b 
import matplotlib.pyplot as plt
import PlasmaBubbles as pb 
import GEO as gg 


args = dict(
    marker = 'o', 
    markersize = 3,
    linestyle = 'none'
    )

b.config_labels()



def plot_epbs_occurrences_roti(
        ds,
        cols = None,
        the = 0.25
        ):

    fig, ax = plt.subplots(
        nrows = 2, 
        dpi = 300, 
        sharex = True, 
        figsize = (11, 6)
        )
    
    ds = ds[[str(c1 * -10) for c1 in cols]]
    
    plt.subplots_adjust(hspace = 0.1)
    
    color = ['k', 'b', 'r', 'g', 'magenta']
    
    dn = ds.index[0]
    
    title = f'Longitudinal zones (threshold = {the} TECU/min)'
    
    for i, col in enumerate(ds.columns):

        line, = ax[0].plot(
            ds[col], 
            color = color[i], 
            **args
            )
        
        ax[0].axhline(
            the, 
            color = 'k', lw = 2, linestyle = '--'
            )
        
        ds1 = pb.events_by_longitude(ds[col], the)
        
        ax[1].plot(
             ds1, 
             marker = 'o',
             markersize = 3,
             color = line.get_color(), 
             label = f'{col}°'
            )
        
        dusk = gg.dusk_time(
                dn,  
                lat = 2, 
                lon = int(col), 
                twilight = 12
                )
        
        ax[1].axvline(
            dusk, 
            linestyle = '--',
            color = line.get_color(), 
            )
    

    ax[0].set(
        yticks = list(range(4)),
        ylabel = 'ROTI (TECU/min)'
        )
    delta = dt.timedelta(hours = 2.1)
    ax[1].text(
        dusk + delta, 
        1.15,
        'Terminators',
        transform = ax[1].transData
        )
    
    ax[1].legend(
        ncol = 5, 
        title = title,
        bbox_to_anchor = (.5, 2.6), 
        loc = "upper center", 
        columnspacing = 0.6
        )
       
    ax[1].set(
        ylabel = 'EPBs occurrence', 
        yticks = [0, 1], 
        xlim = [ds.index[0], ds.index[-1]],
        ylim = [-0.2, 1.4]
        )
     
    b.format_time_axes(ax[1])
    
    ax[0].text(
        0.78, 
        0.53, 
        b.get_infos(dn), 
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
        cols = [8, 7, 6, 5], 
        hours = 13, 
        factor = 8
        ):
        
    infile = f'database/epbs/longs/{dn.year}.txt'
    infile = 'database/longitudes_all_years.txt'
    ds = b.sel_times(
            b.load(infile),
            dn, 
            hours = hours
        )
    
    fig = plot_epbs_occurrences_roti(
            ds, 
            cols
        )
    
    # plt.show()
    
    return fig





dn = dt.datetime(2013, 8, 27, 20)

fig = single_plot(
        dn, 
        cols = [8, 7, 6, 5], 
        hours = 11, 
        factor = 8
        )
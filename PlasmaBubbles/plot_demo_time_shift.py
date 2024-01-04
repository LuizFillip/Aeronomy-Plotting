import datetime as dt
import matplotlib.pyplot as plt
import base as b 
import PlasmaBubbles as pb 

args = dict(
    marker = 'o', 
    markersize = 3,
    linestyle = 'none'
    )


def plot_events(ax, dn):
    
    df = b.load(
        pb.epb_path(
            dn.year, path = 'events'
            )
        ).interpolate()
    
    ds = b.sel_times(df, dn)
    
    ax.plot(ds[col],
            marker = 'o',
            markersize = 3)
    
    ax.set(
        ylabel = 'EPBs occurrence', 
        yticks = [0, 1], 
        xlim = [ds.index[0], 
                ds.index[-1]],
        ylim = [-0.2, 1.2]
        )
    
    for limit in [0, 1]:
        ax.axhline(
            limit, 
            color = 'k', 
            linestyle = '--'
            )
        
    return ds

def plot_long(ax, dn, col):

    df = b.load(
        pb.epb_path(
            dn.year, path = 'longs'
            )
        )
    
    ax.plot(
        b.sel_times(df[col], dn), 
        color = 'k', **args)
    
    ax.set(
        yticks = list(range(5)),
        ylabel = 'ROTI (TECU/min)'
        )
    
    ax.axhline(
        0.25, 
        color = 'r', 
        lw = 2, 
        label = '0.25 TECU/min')
    
    ax.legend(loc = 'upper right')
    
def plot_arrow_and_note(ax, sel):
    
    middle = pb.middle_time(sel)
    
    shift = round(sel['duration'], 2)
    
    ax.annotate(
        '', 
        xy = (sel['start'], 0.5), 
        xytext = (sel['end'], 0.5), 
        arrowprops = dict(arrowstyle='<->')
        )
    
    ax.annotate(
        f'{shift} hrs',
        xy = (middle, 0.55), 
        xycoords = 'data',
        fontsize = 20.0,
        textcoords = 'data', 
        ha = 'center'
        )
    
    
def plot_demo_time_shift(dn, col):
    
    fig, ax = plt.subplots(
        figsize = (12, 6), 
        nrows = 2, 
        sharex = True, 
        dpi = 300 
        )
    
    plot_long(ax[0], dn, col)
    ds = plot_events(ax[1], dn)
    
    
    b.format_time_axes(ax[1])
    
    ds = pb.track_time_diff(ds, col)
    
    for i in range(len(ds)):
        sel = ds.iloc[i, :]
        if sel['duration'] != 0:  
            plot_arrow_and_note(ax[1], sel)





def main():

    col = '-70'
    dn = dt.datetime(2022, 12, 20, 20)
    plot_demo_time_shift(dn, col)
    

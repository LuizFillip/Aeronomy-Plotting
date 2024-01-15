import datetime as dt
import matplotlib.pyplot as plt
import base as b 
import PlasmaBubbles as pb 
import plotting as pl 
import GEO as gg 

b.config_labels(fontsize = 30)

args = dict(
    marker = 'o', 
    markersize = 3,
    linestyle = 'none'
    )

def middle_time(start, end):
    
    return end + (start - end) / 2

def plot_arrow_and_note(ax, start, end, time):
    
    middle = middle_time(start, end)
        
    ax.annotate(
        '', 
        xy = (start, 0.5), 
        xytext = (end, 0.5), 
        arrowprops = dict(arrowstyle='<->')
        )
    
    ax.annotate(
        f'{round(time, 2)}',
        xy = (middle, 0.55), 
        xycoords = 'data',
        fontsize = 30.0,
        textcoords = 'data', 
        ha = 'center'
        )
    

def terminator_time(ax, dn, col):
    
    lon, lat = gg.first_edge(dn.year)[col]
    
    return gg.dusk_time(
            dn, 
            lat = lat, 
            lon = lon, 
            twilight = 18
            )
     
def first_occurrence(ds, col):
    return ds[ds[col] == 1].index.min()

def plot_terminator_shift(ax, dusk, occur):
    
    ax.axvline(dusk, lw = 2, linestyle = '--')
    
    ax.annotate(
        '', 
        xy = (dusk, 0.5), 
        xytext = (occur, 0.5), 
        arrowprops = dict(arrowstyle='<->')
        )
    
    middle = dusk + (occur - dusk) / 2
    dtime = (occur - dusk).total_seconds() / 3600
    
    dtime = round(dtime, 2)
    ax.annotate(
        f'{dtime}',
        xy = (middle, 0.55), 
        xycoords = 'data',
        fontsize = 30.0,
        textcoords = 'data', 
        ha = 'center'
        )
    
    

def plot_demo_time_shift(dn, col):
    
    fig, ax = plt.subplots(
        figsize = (14, 10), 
        nrows = 2, 
        sharex = True, 
        dpi = 300 
        )
    
    plt.subplots_adjust(hspace = 0.05)
    
    df = pb.load_raw_in_sector(dn)
    
    ds = pl.plot_roti_points(ax[0], df, label = True)
    
    events = pl.plot_occurrence_events(ax[1], ds)
    
    ds = pb.track_time_diff(events, col = 'max')
    
    dusk = terminator_time(ax, dn, col)
    
    occur = first_occurrence(events, col = 'max')
    
    plot_terminator_shift(ax[1], dusk, occur)
    
    for i in range(len(ds)):
        sel = ds.iloc[i, :]
        start = sel['start']
        end = sel['end']
        time = sel['duration']
        
        if sel['duration'] > 1:  
            
            plot_arrow_and_note(ax[1], start, end, time)
    
    b.format_time_axes(ax[1], translate = True)
    

    return fig 



def main():

    col = -50
    
    dn = dt.datetime(2014, 2, 9, 21)
    fig = plot_demo_time_shift(dn, col)
    
    plt.show()
    
main()


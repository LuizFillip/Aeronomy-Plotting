import datetime as dt
import matplotlib.pyplot as plt
import base as b 
import PlasmaBubbles as pb 
import GEO as gg 

b.config_labels(fontsize = 25)

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
    




def dusk(dn, col):
    
    lon, lat = gg.first_edge(dn.year)[int(col)]
    
    return gg.dusk_time(dn, lat = lat, lon = lon, twilight = 18)

def plot_terminator_shift(ax, dusk, occur):

    ax.annotate(
        '', 
        xy = (dusk, 0.5), 
        xytext = (occur, 0.5), 
        arrowprops = dict(arrowstyle='<->')
        )
    
    middle = middle_time(occur, dusk)
    dtime = round((occur - dusk).total_seconds() / 3600, 2)
        
    ax.annotate(
        f'{dtime}',
        xy = (middle, 0.55), 
        xycoords = 'data',
        fontsize = 30.0,
        textcoords = 'data', 
        ha = 'center'
        )
    
def plot_shift(ax, ds, col):
    
    dn = ds.index[0]
    occur = ds[ds[col] == 1].index.min()
    
    ds = pb.track_time_diff(ds, col, floatType = False)
  
    plot_terminator_shift(ax, dusk(dn, col), occur)
    
    for i in range(len(ds)):
        sel = ds.iloc[i, :]
        start = sel['start']
        end = sel['end']
        time = sel['duration']     
            
        plot_arrow_and_note(ax, start, end, time)


def plot_occurrencegram(ax, ds, threshold = 0.25):
    dn = ds.index[0]
    col = ds.name
    ds1 = pb.events_by_longitude(ds, threshold)
    
    ax.plot(
         ds1, 
         marker = 'o',
         markersize = 3,
         color = 'k', 
         label = f'{col}°'
        )
        
    ax.axvline(
        dusk(dn, col), 
        linestyle = '--',
        color = 'k', 
        )
    
    b.format_time_axes(ax, translate = True)
    
    return ds1


def plot_roti_max(ax, ds, threshold = 0.25):
    
    col = ds.name
    ax.plot(ds)
    
    ax.axvline(
        dusk(dn, col), 
        linestyle = '--',
        color = 'k', 
        )
    
    ax.axhline(
         threshold, 
         color = 'red', lw = 2, 
         label = f'{threshold} TECU/min'
         )





def plot_epb_time_feadtures(ds,  col = '-50'):

    fig, ax = plt.subplots(
          figsize = (14, 8), 
          nrows = 2, 
          sharex = True, 
          dpi = 300 
          )
      
    plt.subplots_adjust(hspace = 0.05)

    plot_roti_max(ax[0], ds[col])
    
    events = plot_occurrencegram(ax[1], ds[col])
    
    
    plot_shift(ax[1], events, col)
    return fig

df = b.load('database/longitudes_all_years.txt')


dn = dt.datetime(2013, 2, 2, 20)


ds = b.sel_times(df, dn, hours = 11)

fig = plot_epb_time_feadtures(ds,  col = '-50')
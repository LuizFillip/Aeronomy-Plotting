import datetime as dt
import matplotlib.pyplot as plt
import base as b 
import PlasmaBubbles as pb 
import GEO as gg 
import plotting as pl 

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
    
def plot_shift(ax, ds, col, lon = -50):
    
    dn = ds.index[0]
    occur = ds[ds[col] == 1].index.min()
    
    ds = pb.track_time_diff(ds, 'max', floatType = False)
  
    plot_terminator_shift(ax, dusk(dn, lon), occur)
    
    for i in range(len(ds)):
        sel = ds.iloc[i, :]
        start = sel['start']
        end = sel['end']
        time = sel['duration']     
            
        plot_arrow_and_note(ax, start, end, time)

def plot_terminator_line(ax, dn, lon, vmax = 5, label = False):
    
    delta = dt.timedelta(minutes = 30)
    dusk_time = dusk(dn, lon)  - delta
    
    ax.axvline(
        dusk_time, 
        linestyle = '--',
        color = 'k', 
        lw = 2
        )
    
    if label:
      
        ax.text(
            dusk_time, 
            vmax,
            'Solar terminator (300 km)',
            transform = ax.transData
            )
    
    return 
def plot_occurrencegram(ax, ds, lon = -50, threshold = 0.25):
    dn = ds.index[0]
   
    ds1 = pb.events_by_longitude(ds, threshold)
    
    ax.plot(
         ds1, 
         marker = 'o',
         markersize = 3,
         color = 'k', 
         label = f'{lon}°'
        )
    
    
    plot_terminator_line(ax, dn, lon, label = False)
    
    for limit in [0, 1]:
        ax.axhline(
            limit, 
            color = 'k', 
            linestyle = '--'
            )
    
    ax.set(
        ylabel = 'EPBs occurrence', 
        yticks = [0, 1], 
        xlim = [ds.index[0], ds.index[-1]],
        ylim = [-0.2, 1.2]
        )
    
    b.format_time_axes(ax, translate = False)
    
    return ds1


def plot_roti_max(ax, ds, lon = -50, threshold = 0.25):
    
    ds1 = pl.plot_roti_points(
            ax, ds, 
            threshold = threshold,
            label = True, 
            points_max = True, 
            occurrence = False
            )
    
    plot_terminator_line(ax, dn, lon, label = True)
    
    ax.axhline(
         threshold, 
         color = 'red', lw = 2, 
         label = f'{threshold} TECU/min'
         )
    
    pl.legend_max_points_roti(ax, fontsize = 25)
    
    return ds1





def plot_epb_time_feadtures(ds,  col = '-50'):

    fig, ax = plt.subplots(
          figsize = (14, 8), 
          nrows = 2, 
          sharex = True, 
          dpi = 300 
          )
      
    plt.subplots_adjust(hspace = 0.05)


    ds1 = plot_roti_max(ax[0], ds, lon = -50)
    
    events = plot_occurrencegram(ax[1], ds1['max'], lon = -50)
    
    plot_shift(ax[1], events, col = 'max')
    return fig

import os 


dn = dt.datetime(2013, 1, 14, 20)

df = pb.concat_files(
     dn, 
     days = 2, 
     root = os.getcwd(), 
     hours = 12
     )

fig = plot_epb_time_feadtures(df,  col = '-50')


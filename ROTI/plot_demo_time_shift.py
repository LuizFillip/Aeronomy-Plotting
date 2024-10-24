import datetime as dt
import matplotlib.pyplot as plt
import base as b 
import PlasmaBubbles as pb 
import GEO as gg 
import plotting as pl 

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
    time = str(round(time, 2)).replace('.', ',')
    
    ax.annotate(
        f'{time} hrs',
        xy = (middle, 0.55), 
        xycoords = 'data',
        fontsize = 30.0,
        textcoords = 'data', 
        ha = 'center'
        )
    


    return None 

def dusk(dn, col):
    
    lon, lat = gg.first_edge(dn.year)[int(col)]
    
    return gg.dusk_time(dn, lat = lat, 
                        lon = lon, twilight = 18)

def plot_terminator_shift(ax, dusk, occur):

    ax.annotate(
        '', 
        xy = (dusk, 0.5), 
        xytext = (occur, 0.5), 
        arrowprops = dict(arrowstyle='<->')
        )
    
    middle = middle_time(occur, dusk)
    
    dtime = abs(round(
        (occur - dusk).total_seconds() / 3600, 2))
    
    dtime = str(dtime).replace('.', ',')
    
    ax.annotate(
        f'{dtime} hrs',
        xy = (middle, 0.55), 
        xycoords = 'data',
        fontsize = 30.0,
        textcoords = 'data', 
        ha = 'center'
        )
    
    
    middle = middle_time(occur, dusk)
    # info = middle.strftime('Primeira ocorrência em %Hh%M UT')
    
    #
    
    return None 
    
    
    
def plot_shift(ax, ds, col, lon = -50):
    
    dn = ds.index[0]
    occur = ds[ds[col] == 1].index.min()
    
    ds = pb.track_time_diff(
        ds, 'max', floatType = False)
  
    plot_terminator_shift(ax, dusk(dn, lon), occur)
    
    for i in range(len(ds)):
        sel = ds.iloc[i, :]
        start = sel['start']
        end = sel['end']
        time = sel['duration']     
        if time > 2:
            plot_arrow_and_note(ax, start, end, time)

    
    return None 


def plot_terminator_line(
        ax, 
        dn, 
        lon, 
        vmax = 5, 
        label = False):
    
    # delta = dt.timedelta(minutes = 30)
    dusk_time = dusk(dn, lon) # - delta
    
    ax.axvline(
        dusk_time, 
        linestyle = '--',
        color = 'k', 
        lw = 2
        )
    
    if label:
        ax.text(
            dusk_time, 5.1, 
                'Terminadouro local',
            transform = ax.transData)
    return None


def plot_occurrencegram(
        ax, 
        ds, 
        lon = -50, 
        threshold = 0.25
        ):
    
    dn = ds.index[0]
    times = pb.time_range(ds)
    ds1 = pb.maximum_in_time_window(ds, 'max', times)
    
   
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
    
    return ds1


def plot_roti_max(
        ax, ds, 
        lon = -50, 
        threshold = 0.272
        ):
    
    target = ds.index[-1]
    
    ds = pb.filter_region_and_dn(ds, target, lon)
        
    dn = ds.index[0]
    
    
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
         color = 'red', 
         lw = 2, 
         label = f'{threshold} TECU/min'
         )
    
    pl.legend_max_points_roti(
        ax, 
        threshold = threshold,
        fontsize = 25,
        anchor = (0.8, 2))
    
    return ds1





def plot_epb_time_feadtures(
        ds,  
        col = '-50', 
        translate = False,
        threshold = 0.20
        ):

    fig, ax = plt.subplots(
          figsize = (14, 8), 
          nrows = 2, 
          sharex = True, 
          dpi = 300 
          )
      
    plt.subplots_adjust(hspace = 0.05)

    ds = plot_roti_max(ax[0], ds, int(col), threshold)
    
    times = pb.time_range(ds)
    
    ds = pb.maximum_in_time_window(ds, 'max', times)
    
    
    events = pl.plot_occurrence_events(
        ax[1], ds, threshold)
    
    ax[0].set(ylim = [0, 5], 
              yticks = list(range(0, 6, 1)))
    
    if translate:
        ylabel = 'Occurrence'
    else:
        ylabel = 'Ocorrência'
        
    ax[1].set(
        ylabel = ylabel, 
        yticks = [0, 1], 
        xlim = [ds.index[0], ds.index[-1]],
        ylim = [-0.2, 1.2]
        )
    
    dn = ds.index[0]
    b.format_time_axes(ax[-1], translate = False)
    plot_terminator_line(
        ax[-1], dn, lon = -50, label = False)
    plot_shift(ax[1], events, col = 'max')
    
    b.plot_letters(
        ax, y = 0.8, x = 0.02, 
        fontsize = 40)
    return fig


def main():
    import os 
    
    dn = dt.datetime(2013, 12, 24, 20)
    
    df = pb.concat_files(
         dn, 
         days = 2, 
         root = 'E:\\', 
         hours = 11
         )
    
    fig = plot_epb_time_feadtures(df,  col = '-50')
    
    FigureName = dn.strftime('occurrence_%Y%m%d')
    

    fig.savefig(
          b.LATEX(FigureName, folder = 'timeseries'),
          dpi = 400
          )
    plt.show()
    
    
# main()
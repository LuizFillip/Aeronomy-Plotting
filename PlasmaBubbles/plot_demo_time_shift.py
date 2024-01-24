import datetime as dt
import matplotlib.pyplot as plt
import base as b 
import PlasmaBubbles as pb 
import plotting as pl 
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
    

def terminator_time(ax, dn, col):
    
    lon, lat = gg.first_edge(dn.year)[col]
    
    lon, lat = -30, 0
    dusk = gg.dusk_time(
            dn, 
            lat = lat, 
            lon = lon, 
            twilight = 18
            )
    label = 'Terminadouro solar'
    ax.axvline(
        dusk, 
        lw = 2, 
        linestyle = '--', 
        
        )
    d = dt.timedelta(hours = 0.1)
    ax.text(dusk + d, 1.1, label, 
            transform = ax.transData)
    
    return dusk
     
def to_brazilian(dtime):
    return str(round(dtime, 2)).replace('.', ',')

def plot_terminator_shift(ax, dusk, occur):

    ax.annotate(
        '', 
        xy = (dusk, 0.5), 
        xytext = (occur, 0.5), 
        arrowprops = dict(arrowstyle='<->')
        )
    
    middle = middle_time(occur, dusk)
    dtime = (occur - dusk).total_seconds() / 3600
    
    dtime = to_brazilian(dtime)
    
    ax.annotate(
        f'{dtime} horas',
        xy = (middle, 0.55), 
        xycoords = 'data',
        fontsize = 30.0,
        textcoords = 'data', 
        ha = 'center'
        )
    
def plot_shift(ax, events, dusk):
    
    ds = pb.track_time_diff(events, col = 'max')
  
    occur = events[events['max'] == 1].index.min()
    
    plot_terminator_shift(ax, dusk, occur)
    
    for i in range(len(ds)):
        sel = ds.iloc[i, :]
        start = sel['start']
        end = sel['end']
        time = sel['duration']
        
        if sel['duration'] > 1:  
            
            plot_arrow_and_note(ax, start, end, time)

def plot_demo_time_shift(dn, col):
    
    fig, ax = plt.subplots(
        figsize = (14, 8), 
        nrows = 2, 
        sharex = True, 
        dpi = 300 
        )
    
    plt.subplots_adjust(hspace = 0.05)
    
    # df = pb.load_raw_in_sector(dn)
    
    df = pb.concat_files(dn, root = 'D:\\')

    df = b.sel_times(df, dn, hours = 11)

    lon_min = -48
    
    df =  df.loc[(df['lon'] > lon_min) ]
    
    ds = pl.plot_roti_points(ax[0], df, label = True)
    
    events = pl.plot_occurrence_events(ax[1], ds)
    
    dusk = terminator_time(ax[1], dn, col)
    
    plot_shift(ax[1], events, dusk)
    
    b.format_time_axes(ax[1], translate = True)
    
    
    ax[0].legend(loc = 'upper right', ncol = 1)
    
    b.plot_letters(ax, x = 0.02, y = 0.85, offset = 1)

    return fig 



def main():

    col = -50
    
    dn = dt.datetime(2013, 12, 24, 20)
    fig = plot_demo_time_shift(dn, col)
    FigureName = dn.strftime('sunset_event_%Y%m%d')
    fig.savefig(
        b.LATEX(FigureName, 
                folder = 'timeseries'),
        dpi = 400
        )

    plt.show()
    
main()


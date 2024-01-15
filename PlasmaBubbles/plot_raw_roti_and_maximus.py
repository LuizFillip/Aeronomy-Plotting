import matplotlib.pyplot as plt 
import base as b
import datetime as dt  
import PlasmaBubbles as pb 
import GEO as gg 

b.config_labels()


args = dict(
     marker = 'o', 
     markersize = 3,
     linestyle = 'none', 
     color = 'gray', 
     alpha = 0.2, 
     )
    


def plot_roti_points(ax, ds, threshold = 0.25):
        
    ax.plot(ds['roti'], **args, label = 'ROTI points')
    
    if len(ds) != 0:
        times = pb.time_range(ds)
        
        ax.axhline(0.25, color = 'red', lw = 2, 
                    label = f'{threshold} TECU/min')
        
        df1 = pb.time_dataset(ds, 'max', times)
        
        ax.plot(df1, 
                color = 'k',
                marker = 'o', 
                markersize = 3, 
                linestyle = 'none',
                label = 'Maximum value')
        
        ax.set(yticks = list(range(0, 5)))
    
        return df1['max']

def plot_occurrence_events(ax, ds):
    
    events = pb.events_by_longitude(ds, 0.25)
    ax.plot(
          events, 
          marker = 'o',
          markersize = 3,
          color = 'k'
        )
    
    ax.set(
        ylabel = 'EPBs occurrence', 
        yticks = [0, 1], 
        xlim = [ds.index[0], ds.index[-1]],
        ylim = [-0.2, 1.4]
        )
    
    b.format_time_axes(ax)
    
    for limit in [0, 1]:
        ax.axhline(
            limit, 
            color = 'k', 
            linestyle = '--'
            )
        
    return events
        

        


def plot_raw_roti_maximus_events(dn):
    
    '''
    Plot only one region by date

    '''
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 2,
        sharex= True,
        figsize = (12, 6)
        )
    
    plt.subplots_adjust(hspace= 0.1)
    
    dusk = gg.dusk_time(
            dn,  
            lat = -2.53, 
            lon = -44.296, 
            twilight = 12
            )
    
    ax[0].set(ylabel = 'ROTI (TECU/min)')
    
    ax[0].legend(loc = 'upper right')
    
    ax[1].axvline(dusk, label = 'Region E terminator')
    
    ax[1].legend(loc = 'upper right')
    
    df = pb.load_raw_in_sector(dn)
    
    df1 = plot_roti_points(ax[0], df, threshold = 0.25)
    
    plot_occurrence_events(ax[1], df1)
    
    return fig

def main():
    
    dn = dt.datetime(2013, 12, 24, 20)
    
    fig = plot_raw_roti_maximus_events(dn)
    
    # FigureName = 'raw_roti_maximus_events'
    
    # fig.savefig(
    #       b.LATEX(FigureName, 
    #       folder = 'timeseries'),
    #       dpi = 400
    #       )
    
#   s
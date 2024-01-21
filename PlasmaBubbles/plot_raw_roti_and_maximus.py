import matplotlib.pyplot as plt 
import base as b
import datetime as dt  
import PlasmaBubbles as pb 
import GEO as gg 
import numpy as np

b.config_labels()


args = dict(
     marker = 'o', 
     markersize = 3,
     linestyle = 'none', 
     color = 'gray', 
     alpha = 0.2, 
     )
    


def plot_roti_points(
        ax, ds, 
        threshold = 0.25,
        label = False
        ):
        
    ax.plot(ds['roti'], **args, 
            label = 'Pontos de ROTI')
    
    vmax = np.ceil(ds['roti'].values.max())
    
    if len(ds) != 0:
        times = pb.time_range(ds)
        
        ax.axhline(
            threshold, 
            color = 'red', lw = 2, 
            label = f'{threshold} TECU/min'
            )
        
        df1 = pb.time_dataset(ds, 'max', times)
        
        ax.plot(df1, 
                color = 'k',
                # marker = 'o', 
                markersize = 3, 
                # linestyle = 'none',
                label = 'Valor máximo')
        
        ax.set(yticks = np.arange(0, vmax + 2, 1))
        
        if label:
            ax.set(ylabel = 'ROTI (TECU/min)')
    
        return df1['max']

def plot_occurrence_events(ax, ds, threshold = 0.4):
    
    events = pb.events_by_longitude(ds, threshold)
    ax.plot(
          events, 
          marker = 'o',
          markersize = 3,
          color = 'k'
        )
    
    ax.set(
        ylabel = 'Ocorrência', 
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
            lat = 0, 
            lon = -30, 
            twilight = 12
            )
    
    
    
    ax[1].axvline(dusk, lw = 2, linestyle = '--')
    
    
    
    # df = pb.load_raw_in_sector(dn)
    
    dn = dt.datetime(2013, 12, 24, 20)

    df = pb.concat_files(dn, root = 'D:\\')

    df = b.sel_times(df, dn, hours = 11)

    lat_min = -12 
    lon_min = -48
    
    df =  df.loc[(df['lon'] > lon_min) ]
    
    
    df1 = plot_roti_points(ax[0], df, threshold = 0.4, label = True)
    
    plot_occurrence_events(ax[1], df1)
    
    b.plot_letters(ax, x = 0.02, y = 0.85)
    
    ax[0].legend(loc = 'upper right')
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
    
main()

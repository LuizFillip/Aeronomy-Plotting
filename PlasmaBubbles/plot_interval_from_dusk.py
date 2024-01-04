import PlasmaBubbles as pb 
import base as b
import datetime as dt 
import matplotlib.pyplot as plt 


b.config_labels()

args = dict(
    marker = 'o', 
    markersize = 3,
    linestyle = 'none'
    )


def plot_text_time(ax, dusk):
    
    time_str = dusk.strftime('%H:%M')
    
    ax.text(
        dusk, 
        1.25, 
        time_str, 
        transform = ax.transData
        )
    
def plot_arrow_range(ax, dusk, occur):
    

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
        f'$\\delta t =$ {dtime}',
        xy = (middle, 0.55), 
        xycoords = 'data',
        fontsize = 20.0,
        textcoords = 'data', 
        ha = 'center'
        )


def plot_dusk_ln(ax, dn, col):
    
    long = int(col) + 10
    
    dusk = pb.dusk_time(dn, long)
    
    ax.axvline(dusk, lw = 2, linestyle = '--')
    
    ds = pb.set_data(dn, pb.PATH_EVENT) 
    
    occur = ds[ds[col] == 1].index.min()
       
    plot_arrow_range(ax, dusk, occur)
    
   
    for tm in [dusk, occur]:
        
        plot_text_time(ax, tm)

def plot_time_difference(dn):
    
    ds = pb.set_data(dn, pb.PATH_LONG) 
    col = str(-40)
    
    fig, ax = plt.subplots(
        nrows = 2, 
        dpi = 300, 
        sharex = True, 
        figsize = (12, 6)
        )
    
    plt.subplots_adjust(hspace = 0.2)
    
    
    for col in ['-40', '-70']:
        the = pb.threshold(dn, col)
         
        plot_dusk_ln(ax[1], dn, col)
        
        line, = ax[0].plot(
            ds[col], 
            # color = 'r', 
            **args, 
            label = f'Longitude = {col}°'
            )
        
        ax[0].axhline(
            the, 
            color = line.get_color(), 
            # label = f'Threshold = {the} TECU/min'
            )
        
    
        ax[1].plot(
             pb.get_events_series(ds[col]), 
             marker = 'o',
             markersize = 2,
             color = line.get_color()
            )
        
        ax[0].legend(
            loc = 'upper right', 
            ncol = 2)
        
        ax[0].set(
            ylim = [0, 5], 
            yticks = list(range(6)),
            ylabel = 'ROTI (TECU/min)'
            )
        
        ax[1].set(
            ylabel = 'EPBs occurrence', 
            xlim = [ds.index[0],  ds.index[-1]],
            yticks = [0, 1], 
            ylim = [-0.2, 1.2]
            )
        
        for limit in [0, 1]:
            ax[1].axhline(
                limit, 
                color = 'k', 
                linestyle = '--'
                )
            
            
    b.format_time_axes(ax[1])
    

    return fig
    

dn = dt.datetime(2013, 1, 12, 20, 0)

fig = plot_time_difference(dn)



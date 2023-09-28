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

def plot_dusk_ln(ax, dn, col):
    
    long = int(col) + 10
    
    dusk = pb.dusk_time(dn, long)
    
    ax.axvline(dusk, lw = 2, linestyle = '--')
    
    time_str = dusk.strftime('%H:%M (UT)')
    
    ax.text(
        dusk, 
        1.25, 
        time_str, 
        transform = ax.transData
        )
    
    ds = pb.set_data(dn) 
    first_occu = ds[ds[col] == 1].index.min()
    
    ax.annotate('', xy=(dusk, 0.5), 
                xytext=(first_occu, 0.5), 
                arrowprops=dict(arrowstyle='<->'))
    
    middle = dusk + (first_occu - dusk) / 2
    
    ax.annotate('$\\delta t$',
                xy = (middle, 0.55), 
                xycoords='data',
                fontsize= 30.0,
                textcoords='data', 
                ha='center')





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
                    
    the = pb.threshold(dn, col)
     
    plot_dusk_ln(ax[1], dn, col)
    
    line, = ax[0].plot(
        ds[col], 
        color = 'r', 
        **args
        )
    
    ax[0].axhline(
        the, 
        color = line.get_color(), 
        label = f'threshold = {the} TECU/min'
        )
    

    ax[1].plot(
         pb.get_events_series(ds[col]), 
         marker = 'o',
         markersize = 2,
         color = line.get_color(), 
         label = f'Longitude = {col}°'
        )
    
    ax[0].legend(loc = 'upper left')
    
    ax[1].legend(
        bbox_to_anchor = (.5, 2.6), 
        loc = "upper center"
        )
    
    ax[0].set(ylim = [0, 3], 
              yticks = list(range(4)),
              ylabel = 'ROTI (TECU/min)'
              )
    
    ax[1].set(ylabel = 'EPBs occurrence', 
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
    

dn = dt.datetime(2017, 4, 23, 20, 0)

fig = plot_time_difference(dn)



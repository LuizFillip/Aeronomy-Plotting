import PlasmaBubbles as pb 
import base as b
import datetime as dt 
import matplotlib.pyplot as plt 


b.config_labels()

args = dict(
    marker = 'o', 
    markersize = 3,
    linestyle = 'none', 
    alpha = 0.3
    )

def plot_dusk_ln(ax, dusk):
    
    ax.axvline(dusk, lw = 2, linestyle = '--')
    
    time_str = dusk.strftime('%H:%M')
    
    ax.text(
        dusk - dt.timedelta(hours = 0.9), 
        1.25, 
        time_str, 
        transform = ax.transData
        )



def plot_time_difference(dn):
    
    ds = pb.set_data(dn, pb.PATH_LONG) 
    cols = ds.columns[::-1]
    
    fig, ax = plt.subplots(
        nrows = len(cols), 
        dpi = 300, 
        sharex = True, 
        sharey = True, 
        figsize = (12, 10)
        )
    
    plt.subplots_adjust(hspace = 0.1)
        
    color = ['k', 'b', 'r', 'g', 'magenta']
    
    for i, col in enumerate(cols):
        
        the = pb.threshold(dn, col)
        
        long = int(col) + 10
        
        dusk = pb.dusk_time(dn, long)
        
        plot_dusk_ln(ax[i], dusk)
        
        line, = ax[i].plot(
            ds[col], 
            label = f'{col}° ({the})', 
            color = color[i], 
            **args
            )
        
        ax[i].axhline(
            the, 
            color = line.get_color()
            )
        
        ax[i].legend(loc = 'upper right')
        
        ax1 = ax[i].twinx()
        
        ax1.plot(
             pb.get_events_series(ds[col]), 
             marker = 'o',
             markersize = 2,
             color = line.get_color()
            )
        
        ax[i].set(ylim = [0, 5], 
                  yticks = list(range(5)))
        
        ax1.set(
            xlim = [ds.index[0],  ds.index[-1]],
            yticks = [0, 1], 
            ylim = [-0.2, 1.2]
            )
        
        for limit in [0, 1]:
            ax1.axhline(
                limit, 
                color = 'k', 
                linestyle = '--'
                )
            
            
    b.format_time_axes(ax[4])
    
    # fig.text(
    #     .07, 0.4, 
    #     "ROTI (TECU/min)", 
    #     rotation = "vertical", 
    #     fontsize = 25
    #     )
    plt.show()
    

dn = dt.datetime(2017, 4, 23, 20, 0)

plot_time_difference(dn)



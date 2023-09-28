import PlasmaBubbles as pb 
import base as b
import datetime as dt 
import matplotlib.pyplot as plt 


b.config_labels()

def plot_dusk_ln(ax, dusk):
    
    ax.axvline(dusk, lw = 2, linestyle = '--')
    
    time_str = dusk.strftime('%H:%M')
    
    ax.text(
        dusk, 
        1.1, 
        time_str, 
        transform = ax.transData
        )


def plot_time_difference(dn, ds):
    
    ds = pb.set_data(dn) 
    cols = ds.columns[::-1]
    
    fig, ax = plt.subplots(
        nrows = len(cols), 
        dpi = 300, 
        sharex = True, 
        sharey = True, 
        figsize = (10, 10)
        )
    
    plt.subplots_adjust(hspace = 0.3)
    
    c = b.chars()
    
    for i, col in enumerate(cols):
        
        ax[i].plot(ds[col])
        
        long = int(col) + 10
        
        dusk = pb.dusk_time(dn, long)
        
        plot_dusk_ln(ax[i], dusk)
    
        info =  f'({c[i]}) {col}°'
        ax[i].text(
            0.85, 0.75, 
            info, 
            transform = ax[i].transAxes
            )
        
    ax[4].set(
        xlim = [ds.index[0], 
                ds.index[-1]]
        )
    b.format_time_axes(ax[4])
    
    fig.text(
        .07, 0.4, 
        "ROTI (TECU/min)", 
        rotation = "vertical", 
        fontsize = 25
        )
    

dn = dt.datetime(2013, 1, 1, 20, 0)

plot_time_difference(dn)
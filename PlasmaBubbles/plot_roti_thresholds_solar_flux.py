import PlasmaBubbles as pb 
import matplotlib.pyplot as plt 
import base as b
    
lon = -50
ds = b.load(pb.STATS_PATH)
ds = ds.loc[(ds['lon'] == int(lon))]

ds['value'] = pb.set_value(
    ds['mean'], 
    ds['f107a'], 
    ds['base']
    )

    

def plot_roti_thresholds_flux(ds):
    

    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 3, 
        sharex = True, 
        figsize = (12, 10)
        )
    
    plt.subplots_adjust(hspace = 0.05)
    
    ax[0].plot(ds['f107'])
    ax[0].plot(ds['f107a'], lw = 2)
    ax[0].set(
        ylim = [50, 250], 
        ylabel = '$F_{10.7}$ (sfu)'
        )
    
    ax[1].plot(
        ds[['mean', 'base']], 
        label = ['mean', 'base']
        )
    
    ax[1].set(
        ylabel = 'ROTI (TECU/min)'
        )
    ax[2].plot(ds['value'])

    ax[2].set(
        ylabel = 'Threshold (TECU/min)',
        xlim = [ds.index[0], ds.index[-1]], 
        xlabel = 'Years'
        )
    
    for limit in [0.3, 1]:
        ax[2].axhline(limit, lw = 2, color = 'r')
    

plot_roti_thresholds_flux(ds)
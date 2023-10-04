import PlasmaBubbles as pb 
import matplotlib.pyplot as plt 
import base as b
    

def plot_roti_thresholds_flux(ds):
    

    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 3, 
        sharex = True, 
        figsize = (12, 10)
        )
    
    plt.subplots_adjust(hspace = 0.05)
    
    ax[0].plot(ds['f107'])
    ax[0].plot(
        ds['f107a'], 
        lw = 2, label = 'mean 81 days')
    
    ax[0].set(
        ylim = [50, 250], 
        ylabel = '$F_{10.7}$ (sfu)'
        )
    
    ax[1].plot(
        ds[['mean', 'base']], 
        label = ['$\mu_{max}$', 'Base']
        )
    
    ax[1].legend(loc = 'upper right')
    
    ax[1].set(
        ylabel = 'ROTI (TECU/min)'
        )
    ax[2].plot(ds['value'])

    ax[2].set(
        ylabel = '$\Gamma$ (TECU/min)',
        xlim = [ds.index[0], ds.index[-1]], 
        xlabel = 'Years'
        )
    
    for limit in [0.3, 1]:
        ax[2].axhline(limit, lw = 2, color = 'r')
        
    c = b.chars()

    for i, ax in enumerate(ax.flat):
         
         ax.text(
             0.02, 0.85, f'({c[i]})', 
             transform = ax.transAxes
             )
    
lon = -50
ds = b.load(pb.STATS_PATH)
ds = ds.loc[(ds['lon'] == int(lon))]

ds['value'] = pb.set_value(
    ds['mean'], 
    ds['f107a'], 
    ds['base']
    )

    

plot_roti_thresholds_flux(ds)
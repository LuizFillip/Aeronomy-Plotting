import matplotlib.pyplot as plt
import base as b
import PlasmaBubbles as pb
from math import ceil 

def plot_month(
        ax, 
        ds, 
        flux = 'f107a', 
        roti = 'mean',
        norm = True
        ):
    
    x = ds[flux].values
    y = ds[roti].values
    
    if norm:
        x /= 100
    
    ax.scatter(x, y, s = 5)
    
    fit = b.linear_fit(x, y)
    
    a1, b1 = fit.coeficients
        
    ax.plot(x, fit.y_pred, 
            lw = 2, color = 'r')
    
    info = f'$R^2$ = {fit.r2_score}\n$a$ = {a1}\n$b$ = {b1}'
    ax.text(
        0.1, 0.6, 
        info, 
        transform = ax.transAxes
        )
    
    return ax


def plot_roti_vs_solar_flux(
        flux = 'f107a',
        roti = 'mean', 
        lon = -40,
        norm = True
        ):

    
    ds = pb.join_dataset(lon)
    
    fig, ax = plt.subplots(
        dpi = 300, 
        sharex = True, 
        sharey= True,  
        ncols = 4, 
        nrows = 3,
        figsize = (14, 12)
        )
    
    plt.subplots_adjust(wspace = 0.1)
    
    vmax = ceil(ds[roti].max())
    fmax =  ceil(ds[flux].max())
    fmin = 50
    
    if norm:
        fmax /= 100
        fmin /= 100
    
    for i, ax in enumerate(ax.flat):
        ds1 = ds.loc[
            ds.index.month == i + 1]
        
        plot_month(
            ax, 
            ds1, 
            flux = flux, 
            roti = roti, 
            norm = norm
            )
        
        name = ds1.index[0].strftime('%B')
        ax.set(title = name)
        
        ax.set(xlim = [fmin, fmax], 
               ylim = [0, vmax])
        
        
    title = f'ROTI $ = a F10.7 + b$ (longitude = {lon}°)'
    
    
    b.fig_labels(
            fig, 
            fontsize = 30, 
            title = title,
            ylabel = 'ROTI (TECU/min)', 
            xlabel = "F10.7 (SFU)"
            )

    return fig

fig = plot_roti_vs_solar_flux()
import events as ev 
import numpy as np
import matplotlib.pyplot as plt 
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.optimize import curve_fit
import base as b 



def sigmoid(x, a, b):
    
    '''
    Sigmoid function
    '''
    return 1 / (1 + np.exp(-a * x - b))


def data_sigmoid(ax, ds):
    
    
    args =  dict(
        marker = 's', 
        capsize = 5, 
        markersize = 10, 
        linestyle = 'none',
        fillstyle = 'none'
        )
    
    ax.errorbar(
        ds['mean'], 
        ds['rate'], 
        xerr = ds['std'],
        yerr = ds['epb_error'],
        **args
        )
    
    
    x_data, y_data = ds['start'],  ds['rate']
    
    params, covariance = curve_fit(
        sigmoid, x_data, y_data, p0=[1, 1])
    
    x = np.linspace(min(x_data), max(x_data), 100)
    
    ax.plot(x, sigmoid(x, *params), lw = 2, 
            color = 'red', 
            label = '$1 / (1 + e^{-a x - b})$')
    
    for bar in [0, 1]:
        ax.axhline(
            bar, 
            linestyle = ":", 
            lw = 2, 
            color = "k"
            )
        
    ax.legend()
    



def plot_hist_distr(ds):
    

    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (12, 8)
        )
    
    divider = make_axes_locatable(ax)
    
    xhax = divider.append_axes(
        "top", 
        size = 2, 
        pad = 0.1, 
        sharex=ax)
    
    
    args = dict(
        
        edgecolor = 'k')
    
    
    
    
    data_sigmoid(ax, ds)
    
    xhax.bar(
           ds['start'], 
           ds['days'], 
           width = 0.05,
           color = 'k', 
           **args)
    
    b.change_axes_color(
            xhax, 
            color = 'k',
            axis = "y", 
            position = "left"
            )
    
    
    yhax = xhax.twinx()
    
    yhax.bar(
        ds['start']-0.05, 
        ds['epbs'], 
        width = 0.05,
        color = '#0C5DA5',
        **args)
    
    b.change_axes_color(
            yhax, 
            color = '#0C5DA5',
            axis = "y", 
            position = "right"
            )
    
    xlabel = b.y_label('gamma')
    ax.set(
        ylim = [-0.1, 1.1],
        xlabel = xlabel, 
        ylabel = 'EPB occurrence probability',
        yticks = np.arange(0, 1.2, 0.2)
        )
    
  
    vmax = max(ds['days'])
    yhax.set(ylim = [0, vmax], ylabel = 'nights with epb')
    xhax.set(ylim = [0, vmax], ylabel = 'Total in each bin')
    
    plt.setp(xhax.get_xticklabels(), visible=False)
    
    return fig
    
    

df = ev.concat_results('saa')

vmin, vmax, step = 0, 3.8, 0.2


ds = ev.probability_distribuition(
    df,
    limits = (vmin, vmax, step),
    col = 'gamma'
    )

fig = plot_hist_distr(ds)


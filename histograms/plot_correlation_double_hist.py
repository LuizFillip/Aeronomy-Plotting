import events as ev 
import numpy as np
import matplotlib.pyplot as plt 
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.optimize import curve_fit

df = ev.concat_results('saa')

vmin, vmax, step = 0, 3.8, 0.1

df = df.loc[ 
            (df['kp'] > 3)]


ds = ev.probability_distribuition(
    df,
    limits = (vmin, vmax, step),
    col = 'gamma'
    )


def sigmoid(x, a, b):
    
    '''
    Sigmoid function
    '''
    return 1 / (1 + np.exp(-a * x - b))


def data_sigmoid(ax, x_data, y_data):
    
    params, covariance = curve_fit(
        sigmoid, x_data, y_data, p0=[1, 1])
    
    x = np.linspace(min(x_data), max(x_data), 100)
    
    ax.scatter(
        x_data, y_data, 
        s = 100, 
        marker = 's'
        )
    
    
    ax.plot(x, sigmoid(x, *params), lw = 2, 
            color = 'red')





def plot_hist_distr(ds):
    

    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (10, 10))
    
    divider = make_axes_locatable(ax)
    
    xhax = divider.append_axes(
        "top", 
        size = 2, 
        pad = 0.1, 
        sharex=ax)
    
    yhax = divider.append_axes(
        "right", 
        size = 2, 
        pad = 0.1, 
        
        sharey=ax)
    
    args = dict(
        color = 'gray', 
        edgecolor = 'k')
    
    x_data, y_data = ds['start'],  ds['rate']
    
    
    data_sigmoid(ax, x_data, y_data)
    
    xhax.bar(
           ds['start'], 
           ds['days'], 
           width = 0.1,
           **args)

    yhax.barh(
        ds['rate'], 
        ds['epbs'], 
        height = 0.05,
        **args)
    
    ##turning off duplicate ticks:
    plt.setp(xhax.get_xticklabels(), visible=False)
    plt.setp(yhax.get_yticklabels(), visible=False)
    
    ax.set(ylim = [-0.2, 1.2])
    
    

plot_hist_distr(ds)

ds
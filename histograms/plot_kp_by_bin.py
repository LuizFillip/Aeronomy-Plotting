import base as b
import matplotlib.pyplot as plt 
import core as c 
import numpy as np
b.config_labels()

from scipy.stats import norm


start = 1
ds = c.resample_for_the_same_size(
    c.length_by_interval(df, start)
    )

def plot_Kp_by_bin(ds):
        
    bins = np.arange(1, 10, 1)
    
    months = ['march', 'september', 'december']
    
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (14, 8),
        ncols = 3, 
        sharey = True, 
        sharex = True
        )
    
    plt.subplots_adjust(wspace = 0.05)
    
    for i, mon in enumerate(months):
        data = ds[mon]['kp'].values
        
        ax[i].hist(
            data,
            bins = bins,
            density=False,
            color = 'gray', 
            edgecolor = 'k'
            )
        
        mu, std = norm.fit(data)
    
        ax[i].set(title = mon, 
                  xticks = bins,
                  xlabel = 'Kp',
                  ylim = [0, 35])
       
        
        bin_width = bins[1] - bins[0]
    
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(
            x, mu, std) * len(data) * bin_width
        mu = round(mu, 2)
        ax[i].text(
            0.45, 0.9, 
            '$\\bar{Kp} = $' + f'{mu}', 
            transform = ax[i].transAxes
            )
    
        ax[i].plot(x, p, 'k', linewidth=2)
       
    ax[0].set(ylabel = 'Number of cases')
    
    fig.suptitle('$\gamma_{RT} = $' + f'{start} - {start + 0.2}')
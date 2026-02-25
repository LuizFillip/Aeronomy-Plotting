from merra import load_merra 
import pandas as pd 
import numpy as np
import base as b 
import core as c 
import matplotlib.pyplot as plt 
 



def plot_scatter_fit(
        ax, df, 
        color = 'red', 
        marker = 's', 
        label  = ''
        ):
 
    x = df.iloc[:, 0].values
    y = df.iloc[:, 1].values
    
    fit = b.linear_fit(x, y)
    
    corr = np.corrcoef(x, y)[1, 0]
    label = label.capitalize()
    ax.plot(
        x, y, 
        markersize = 10, 
        linestyle = 'none',
        color = color, 
        marker = marker, 
        label = f'{label}', 
        markeredgecolor = 'black',
        markeredgewidth = 2
        )
     
    ax.plot(
        x, fit.y_pred, 
        lw = 2, 
        color = color
        )
    
    ax.set(ylim = [-1, 25])
    ax.text(
        0.65, 0.85, 
        f"r = {corr:.2f}", 
        transform = ax.transAxes, 
        color ='k', 
        fontsize = 25 
        )
    return ax
 

def data_1(start, end):
 
    ds = c.data_epbs(start, end, percent = False)

    ds['dev'] = (ds['september'] -  ds['march'])  
      
    return ds 


def data_2(start, end, col = 'T_60_90_S'):
    df = load_merra()

    ds = c.average_equinox(df[col], start, end) 
    
    ds['dev'] = (ds['september'] -  ds['march'])  
    return ds

def join(tcol, season):
    start, end = 2009, 2024
    y = data_2(start, end, tcol)
    x = data_1(start, end)
    
    return pd.concat([y[season], x[season]], axis = 1)  




 
def plot_correlation_both_hemispheres():
    fig, ax = plt.subplots(
            dpi = 300, 
            ncols = 2, 
            sharey = True,
            figsize = (10, 5)
            )
    
    plt.subplots_adjust(wspace = 0.05)
    
    colors = ['purple', 'purple']
    hemis = ['T_60_90_N', 'T_60_90_S']
     
    for i, hem in enumerate(hemis):
   
        df = join(hem, 'dev')
        plot_scatter_fit(
            ax[i], df,  
            color = colors[i], 
            label = ''
            )
            
    ax[0].set(
        title = 'Northern Hemisphere', 
        xlabel = '$\delta T$ (60°-90°)', 
        ylabel = '$\delta_{EPBs} $'
        )
    ax[1].set(
        title = 'Southern Hemisphere', 
        xlabel = '$\delta T$ (60°-90°)'
        )
    
    b.plot_letters(
            ax, 
            x = 0.04, 
            y = 0.85, 
            offset = 0, 
            fontsize = 30,
            num2white = None
            )
    
    return fig 
    

fig = plot_correlation_both_hemispheres()

 
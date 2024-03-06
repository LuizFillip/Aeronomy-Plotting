import matplotlib.pyplot as plt
import FabryPerot as fp
import pandas as pd 
import base as b 

b.config_labels()

def plot_montly_averages(df):

    dirs = fp.DIRECTIONS
    
    
    fig, ax = plt.subplots(
        figsize = (16, 8), 
        dpi = 300,
        nrows = 2, 
        ncols = 2,
        sharex = True, 
        sharey = True
        )
    
    plt.subplots_adjust(wspace = 0.05)
    for num, ax in enumerate(ax.flat):
        
        ds = pd.pivot(
            df, 
            columns = 'day', 
            index = 'time', 
            values = dirs[num]
            )
        
        ax.plot(ds, alpha = 0.5, color = 'gray')
        ax.plot(ds.mean(axis = 1), color = 'k', lw = 3)
        
        ax.set(title = dirs[num].capitalize())
        ax.axhline(0, lw = 1.5, linestyle = '--')
    
    fontsize = 30
    fig.text(
        0.05, 0.35, 
        'Velocity (m/s)', 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.45, 0.02, 
        'Universal time', 
        fontsize = fontsize, 
        )
    
    fig.suptitle(df.index[0].strftime('%B'))
    
    return fig


# infile = 'FabryPerot/data/FPI/9/'
# df = fp.join_days(infile)
# fig = plot_montly_averages(df)
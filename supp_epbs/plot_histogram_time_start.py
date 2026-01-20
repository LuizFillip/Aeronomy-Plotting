import base as b 
import matplotlib.pyplot as plt 
import core as c 
import numpy as np 

b.sci_format(fontsize = 25)

def set_data():

    path = 'database/epbs/epbs_2013_2023'
    df = b.load(path)
    
    df.loc[df['shift'] <= 4, 'type'] = 'sunset'
    
    df = c.add_geo(df)
    
    df = df.loc[(df.lon == -50) & (df['type'] == 'sunset')]
    
    return df

args = dict(
     facecolor = 'lightgrey', 
     edgecolor = 'black', 
     hatch = '////', 
     color = 'gray', 
     linewidth = 1
     )


def plot_stats(
        ax, arr, unit = "hours", 
        fontsize = 15, 
        x = 0.55, y = 0.8
        ):
    mean = round(np.nanmean(arr), 2)
    std = round(np.nanstd(arr), 2)
    
    
    info_mean = f"$\mu = {mean}$ {unit}\n"
    info_std = f"$\sigma = {std}$ {unit}\n"
  
    ax.text(
       x, y, 
        (info_mean + info_std), 
        fontsize = fontsize, 
        transform = ax.transAxes
        )
    return None 
def plot_historam_time_start(df):
    
     

    fig, ax = plt.subplots(
        dpi = 300, 
        ncols = 2,
        sharey = True, 
        sharex = True, 
        figsize = (12, 6)
        )
    
    
    plt.subplots_adjust(wspace=0.1)
    limit = c.limits_on_parts(df['f107a'], parts = 2)
    high = df.loc[df['f107a'] > limit]
    loww = df.loc[df['f107a'] < limit]
    
    colors = ['blue', 'black']
    titles = [f'$F10.7 > {limit}$ sfu', 
              f'$F10.7 < {limit}$ sfu']
    
    bins = np.arange(21, 25, 0.5)
    
    for i, ds in enumerate([high, loww]):
        
        ds['start'].plot(
            kind = 'hist', 
            ax = ax[i], 
            bins = bins, 
            **args
            )
        
        arr = ds['start'].values 
        
        plot_stats(ax[i], arr, x = 0.5, y = 0.75, fontsize = 25)
        
        ax[i].axvline(
            np.mean(arr), 
            color = 'red', 
            lw = 2
            )
        
        ax[i].set(
            title = titles[i],
            xlabel = 'Universal time'
            )
        
    return fig 
    
    
    
df = set_data()
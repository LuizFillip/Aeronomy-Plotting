import PlasmaBubbles as pb 
import base as b 
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.ticker import AutoMinorLocator
import datetime as dt
import core as c
import plotting as pl  

b.config_labels(fontsize = 30)

def divide_by_geomgnetic_levels(df):
    
    cond = [
        df['kp'] <= 3, 
        (df['kp'] > 3) & 
        (df['kp'] <= 6), 
        df['kp'] > 6]
    
    labels = [
    '$Kp \\leq 3$', '$ 3 < Kp \\leq  6$', "$Kp > 6$"
    ]    
    
    
    return cond, labels
ds = b.load('events_class2')


df = ds.loc[
    (ds['type'] == 'midnight') & 
    (ds['drift'] == 'fresh')# &
    # (ds['lon'] == -50)
    ]



df_source = c.geo_index(eyear = 2023)
df['dst'] = df.index.map(df_source['dst'])


def plot_magnetic_dependency(df, cmap = 'jet'):
    

    fig, ax = plt.subplots(
              dpi = 300, 
              nrows = 4,
              ncols = 2,
              sharex = True, 
              sharey = True,
              figsize = (12, 8)
              )
    
    
    plt.subplots_adjust(hspace = 0.1, wspace = 0.1)
    
    def plot_heatmap(ax, ds):
        df2 = pb.hourly_distribution(ds, step = 1).T 
    
        yticks = df2.index 
        xticks = df2.columns 
        values = df2.values
        
        img = ax.imshow(
              values[::-1],
              aspect = 'auto', 
              extent = [xticks[0], xticks[-1], 
                        yticks[0], yticks[-1]],
              cmap = cmap
              )
        
    cols = np.arange(-80, -40, 10)
    
    for i, col in enumerate(cols):
        
        ds = df.loc[(df['lon'] == col)]
    
        plot_heatmap(ax[i, 0], ds.loc[(ds['dst'] >= -30)])
        plot_heatmap(ax[i, 1], ds.loc[(ds['dst'] < -30)])
        
        

def values_by_season(df):
    
    cols = np.arange(-80, -40, 10)
    
    arr = np.zeros((4, 12, 12))
    
    for i, col in enumerate(cols):
          
        df2 = pb.hourly_distribution(
            df.loc[(df['lon'] == col)],
            step = 1, 
            normalize = False,
            percent = False).T 
        
        arr[i] = df2.values


    return arr



quiet = values_by_season(df.loc[(df['dst'] >= -30)])

distu = values_by_season(df.loc[(df['dst'] < -30)])
    

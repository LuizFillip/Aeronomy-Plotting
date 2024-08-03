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


ds = b.load('events_class2')


df = ds.loc[
    (ds['type'] == 'midnight') & 
    (ds['drift'] == 'fresh')
    ]



df_source = c.geo_index(eyear = 2022)
df['dst'] = df.index.map(df_source['dst'])
df['kp'] = df.index.map(df_source['kp'])



# quiet = df.loc[(df['dst'] > -30)]
quiet = values_by_season( df.loc[(df['kp'] <= 3)])

distu = values_by_season(df.loc[(df['kp'] > 3)])
distu /= np.max(distu)

quiet /= np.max(quiet) 

# def plot_magnetic_dependency(df, cmap = 'jet'):
    

fig, ax = plt.subplots(
          dpi = 300, 
          nrows = 4,
          ncols = 2,
          sharex = True, 
          sharey = True,
          figsize = (12, 8)
          )


plt.subplots_adjust(hspace = 0.1, wspace = 0.1)

def plot_heatmap(ax, values):

    yticks = np.arange(20, 32, 1)
    xticks = np.arange(1, 13, 1)
    
    values = values[::-1] * 100
    
    img = ax.imshow(
          values,
          aspect = 'auto', 
          extent = [xticks[0], xticks[-1], 
                    yticks[0], yticks[-1]],
          cmap = 'jet',
          vmax = 100, 
          vmin = 0
          )
    
    # ax.contourf(
    #     xticks, 
    #     yticks,
    #     values,
    #     cmap = 'jet'
    #     )

for row in range(4):
    plot_heatmap(ax[row, 0], quiet[row])
    # plot_heatmap(ax[row, 1], distu[row])
    

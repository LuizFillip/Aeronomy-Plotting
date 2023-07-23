
import pandas as pd
import matplotlib.pyplot as plt


fig, ax = plt.subplots(
    nrows = 2, 
    sharex = True, 
    sharey = True
    )

def plot_coord(ax, south
               ):
    ds = pd.concat(south, axis = 1)
    ax.plot(ds, color = 'gray', alpha = 0.3)
    ax.plot(ds.mean(axis = 1), color = 'k')
    
    ax.plot(ds['2013-03-16'], color = 'r')
# plot_coord(ax[0], south)
# plot_coord(ax[1], north)
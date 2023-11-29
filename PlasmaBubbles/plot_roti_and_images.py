import matplotlib.pyplot as plt
from skimage import io
from matplotlib.gridspec import GridSpec
import digisonde as dg 
import events as ev 
import os 
import imager as im
import base as b 
import datetime as dt 
from plotting import plot_roti_curves

dn = dt.datetime(2017, 4, 3, 20)




def plot_roti(ax, dn):
    
    infile = f'database/epbs/longs/{dn.year}.txt'

    ds = b.sel_times(
            b.load(infile),
            dn, 
        )
    
    args = dict(
        marker = 'o', 
        markersize = 3,
        linestyle = 'none'
        )
    
    
    ax.plot(
        ds['-60'], 
        **args
        )
    
    ax.set(ylim = [0, 1])
    
    b.format_time_axes(ax)
    
    
fig = plt.figure(
    dpi = 400,
    figsize = (12, 8),
    layout = "constrained"
    )
    
gs2 = GridSpec(2, 4)

gs2.update(
    hspace = 0,  
    wspace = 0
    )
    
ax1 = plt.subplot(gs2[-1, :])

plot_roti(ax1, dn)
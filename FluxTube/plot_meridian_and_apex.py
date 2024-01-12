import cartopy.crs as ccrs
import matplotlib.pyplot as plt 
from plotting import (
    plot_apex_vs_latitude,
    plot_mag_meridians, 
    plot_receivers_coords
    )
from matplotlib.gridspec import GridSpec
import base as b 


def plot_meridian_and_apex(year = 2013):
    
    width = 14
    height = width / 4
    fig = plt.figure(
        figsize = (width, height), 
        dpi = 300,
        # layout = "constrained"
        )
    
    
    gs2 = GridSpec(1, 2)
    
    gs2.update(wspace = 0)
    
    ax1 = plt.subplot(gs2[0, 0])
    
    plot_apex_vs_latitude(ax1)
    
    
    ax2 = plt.subplot(
        gs2[0, 1],
        projection = ccrs.PlateCarree()
        )
    
    
    plot_mag_meridians(ax2, year)
    
    plot_receivers_coords(
            ax2, 
            year, 
            distance = None,
            text = False
            )
    
    for i, a in enumerate([ax1, ax2]):
        l = b.chars()[i]
        a.text(
            0.04, 0.9, f'({l})', 
            transform = a.transAxes
            )
        
    return fig

fig = plot_meridian_and_apex()
    
# fig.savefig(b.LATEX('apex_meridian'), dpi = 400)
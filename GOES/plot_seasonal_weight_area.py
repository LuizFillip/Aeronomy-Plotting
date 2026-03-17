import numpy as np
import GOES as gs
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import base as b
import GEO as gg
from scipy.ndimage import gaussian_filter

def plot_map_occ(ax, grid, smooth = True):
    
    lat_lims = dict(min = -60, max = 10, stp = 10)
    lon_lims = dict(min = -100, max = -30, stp = 15)
    
    gg.map_attrs(
        ax, None, 
        lat_lims = lat_lims, 
        lon_lims = lon_lims, 
        grid = False, 
        degress = None
        )
     
    smooth = gaussian_filter(grid.values, sigma=1)
    
    grid_np = np.asarray(grid, dtype=float)

    smooth = gaussian_filter(grid_np, sigma=1.2)
    
    if smooth.max() > 0:
        smooth = smooth / smooth.max() * grid_np.max()
    
    img = ax.contourf(
        grid.columns,
        grid.index,
        smooth,
        levels = 50,
        # norm = norm,
        cmap="jet", 
    )
    
    return img



seasons = {
    "December": [12, 1, 2],
    "March": [3, 4, 5],
    "June": [6, 7, 8],
    "September": [9, 10, 11],
}

def plot_seasonal_area_weighted(nl, step = 2.0, sigma = 1):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        ncols = 4, 
        figsize = (16, 10),
        subplot_kw = {"projection": ccrs.PlateCarree()},
    )
    plt.subplots_adjust(wspace = 0.02, hspace=0.12)

    axes = ax.flat 
    lat_min = np.round(nl['lat_min'].min())
    lon_min = np.round(nl['lon_min'].min())
    lon_max = np.round(nl['lon_max'].max())
    lat_max = np.round(nl['lat_max'].max())
    
    lon_bins = np.arange(lon_min, lon_max + step, step)
    lat_bins = np.arange(lat_min, lat_max + step, step)
    
    for i, (name, months) in enumerate(seasons.items()):
        nl_season = nl.loc[nl.index.month.isin(months)]
        
        grid =  gs.occurrence_area_weighted(
            nl_season, lon_bins, lat_bins
            )
        
        img = plot_map_occ(axes[i], grid)

        l = b.chars()[i]
        axes[i].set_title(f"({l}) {name}", fontsize=28)

        if i != 0:
            axes[i].set(
                xticklabels=[], 
                xlabel="", 
                ylabel="", 
                yticklabels=[]
                )
            
    anchor = [0.3, 0.78, 0.4, 0.025]
    cax = plt.axes(anchor)
    cbar = fig.colorbar(
        img, 
        ax = ax.ravel().tolist(), 
        orientation = "horizontal",
        cax = cax,
        )

    cbar.set_label("Convection activity (\%)", fontsize=22)
    
    # fig.suptitle(str(year), y=0.98, fontsize=28)
    return fig

 
# nl = b.load("GOES/data/nucleos_40/2013")   

# fig = plot_seasonal_area_weighted(nl, step = 2.0 )

 




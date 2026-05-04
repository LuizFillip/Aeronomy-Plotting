import numpy as np
import GOES as gs
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import base as b
import GEO as gg
import pandas as pd  


def count_grid(data, lon_bins, lat_bins):

    lon_center = (data.lon_min + data.lon_max) / 2
    lat_center = (data.lat_min + data.lat_max) / 2

    H, _, _ = np.histogram2d(
        lat_center,
        lon_center,
        bins=[lat_bins, lon_bins]
    )

    return H



def plot_map(ax, grid, lon_bins, lat_bins, title):

 
    mesh = ax.pcolormesh(
        lon_bins[:-1],
        lat_bins[:-1],
        grid,
        cmap = "jet",
        transform=ccrs.PlateCarree()
    )

    lat_lims = dict(min=-60, max=10, stp=10)
    lon_lims = dict(min=-100, max=-30, stp=15)
    
    gg.map_attrs(
        ax, None, 
        lat_lims = lat_lims, 
        lon_lims = lon_lims, 
        grid = False, 
        degress = None
        )

    plt.colorbar(mesh, label="Event count")
    plt.title(title)

    # plt.show()
    
def season(month):
    if month in [12,1,2]:
        return "DJF"
    elif month in [3,4,5]:
        return "MAM"
    elif month in [6,7,8]:
        return "JJA"
    else:
        return "SON"


df = b.load("GOES/data/nucleos_40/2013")   

daily = df.groupby(pd.Grouper(freq="D"))

step = ''
lon_bins = np.arange(-90, -30, 1)   # resolução 1°
lat_bins = np.arange(-60, 15, 1)

fig, ax = plt.subplots(
    dpi = 300, 
 
    subplot_kw = {"projection": ccrs.PlateCarree()},
)
grid_daily = np.zeros((len(lat_bins)-1, len(lon_bins)-1))

for t, g in daily:
    grid_daily += count_grid(g, lon_bins, lat_bins)
    # print(g)

plot_map(ax, grid_daily, lon_bins, lat_bins, 
         "Daily event accumulation")


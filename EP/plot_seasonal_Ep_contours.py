import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from scipy.ndimage import gaussian_filter
import GEO as gg
import GOES as gs
import base as b

pd.options.mode.chained_assignment = None


SEASONS = {
    "DJF": [12, 1, 2],     # DJF
    "MAM": [3, 4, 5],         # MAM
    "JJA": [6, 7, 8],          # JJA
    "SON": [9, 10, 11],   # SON
}

year = 2013
alt = 100
step = 2
df = gs.load_ep_data(
    year = year,
    alt = alt,
    ep_col = "Ep_mean"
)




def compute_seasonal_mean_grid(
        df, 
        lon_bins, 
        lat_bins, 
        value_col = "Ep_max"
        ):
    """
    Calcula a média espacial em uma grade lat-lon regular.
    Retorna um DataFrame com índice = latitude e colunas = longitude.
    """
    data = df.copy()

    data["lon_bin"] = pd.cut(
        data["lon"],
        bins=lon_bins,
        labels=lon_bins[:-1],
        # include_lowest=True,
        # right=False,
    )

    data["lat_bin"] = pd.cut(
        data["lat"],
        bins=lat_bins,
        labels=lat_bins[:-1],
        # include_lowest=True,
        # right=False,
    )

    grouped = (
        data.groupby(["lat_bin", "lon_bin"], 
                     observed=False)[value_col]
        .mean()
        .unstack("lon_bin")
    )

    # garante grade completa
    grouped = grouped.reindex(
        index=pd.Index(lat_bins[:-1], dtype=float),
        columns=pd.Index(lon_bins[:-1], dtype=float),
    )

    grouped.index = grouped.index.astype(float)
    grouped.columns = grouped.columns.astype(float)

    return grouped


 #%%%%
 




value_col = 'Ep_mean'
lon_bins = gs.make_regular_bins(
    df["lon"].min(), df["lon"].max(), step)

lat_bins = gs.make_regular_bins(
    df["lat"].min(), df["lat"].max(), step)



sigma = 0.8

def join_grids(df, lon_bins, lat_bins, value_col):

    seasonal_grids = {}
    for i, (season_name, months) in enumerate(SEASONS.items()):
        df_season = df.loc[df.index.month.isin(months)]
    
        grid = compute_seasonal_mean_grid(
            df_season,
            lon_bins=lon_bins,
            lat_bins=lat_bins,
            value_col=value_col,
        )
        
        
        seasonal_grids[season_name] = grid
        
    return seasonal_grids
     
    
    
    
 
#%%%%
def plot_season_ep_maps(seasonal_grids, vmin, vmax):
    
    fig, axes = plt.subplots(
        ncols = 4,
        figsize = (16, 8),
        dpi = 300,
        subplot_kw = {"projection": ccrs.PlateCarree()},
    )
    
    plt.subplots_adjust(wspace=0.02, hspace=0.12)

    
    def smooth(grid, sigma):
        
        grid = grid.copy()
        
        smooth = gaussian_filter(grid, sigma=sigma)
        
        return smooth  / np.nanmax(smooth) * np.nanmax(grid)
        
    
    for i, (ax, (season_name, grid)) in enumerate(
            zip(axes, seasonal_grids.items())):
        
        label = b.chars()[i]
        values = smooth(grid.values, sigma)
        img = ax.pcolormesh(
            grid.columns,
            grid.index,
            values,
            cmap="jet", 
            vmin = vmin, 
            vmax = vmax
        )
        
        lat_lims = dict(min=-60, max=10, stp=10)
        lon_lims = dict(min=-100, max=-30, stp=15)
    
        gg.map_attrs(
            ax,
            None,
            lat_lims=lat_lims,
            lon_lims = lon_lims,
            grid = False,
            degress = None,
        )
        ax.set(title = season_name)
        
        if i != 0:
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.set_xlabel("")
            ax.set_ylabel("")
    
    cax = fig.add_axes([0.30, 0.84, 0.40, 0.03])
    
    cbar = fig.colorbar(
        img,
        cax = cax,
        orientation="horizontal",
    )
    cbar.set_label(f"{value_col} (J/kg) at {alt} km ", fontsize=20)
    
    return fig 
seasonal_grids

all_values = np.concatenate([
    g.to_numpy(dtype=float).ravel()
    for g in seasonal_grids.values()
])

vmin = np.nanmin(all_values) if all_values.size else None
vmax = np.nanmax(all_values) if all_values.size else None
 

fig = plot_season_ep_maps(seasonal_grids, vmin, vmax + 10)
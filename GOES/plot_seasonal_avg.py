import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import base as b
import GEO as gg

b.sci_format()
 

def occurrence_percent_grid(nl_season, lon_bins, lat_bins, n_total):
    
    df = nl_season.copy()

    # centro do núcleo
    df["lon"] = (df["lon_min"] + df["lon_max"]) / 2
    df["lat"] = (df["lat_min"] + df["lat_max"]) / 2

    df["lon_bin"] = pd.cut(
        df["lon"], lon_bins,
        labels=lon_bins[:-1], include_lowest=True)
    df["lat_bin"] = pd.cut(
        df["lat"], lat_bins,
        labels=lat_bins[:-1], include_lowest=True)

    df = df.groupby(["lon_bin", "lat_bin"]).size().to_frame('count').reset_index()
          

    df['count']  = (df['count']  / df['count'].max()) * 100

    return  pd.pivot_table(
         df, 
         columns = 'lon_bin', 
         index = 'lat_bin', 
         values = 'count'
         ).interpolate()

def occurrence_percent_grid_bbox(nl_season, lon_bins, lat_bins):
    grid = np.zeros((len(lat_bins)-1, len(lon_bins)-1), dtype=float)
  
    
    n_total = nl_season.index.unique().size

    # acumula por frame (para não contar 2x mesma célula no mesmo timestamp)
    for t, g in nl_season.groupby(level=0):
        marked = set()

        for _, r in g.iterrows():
            x0, x1 = sorted([r.lon_min, r.lon_max])
            y0, y1 = sorted([r.lat_min, r.lat_max])

            # bins cobertos (interseção)
            j0 = np.searchsorted(lon_bins, x0, side="right") - 1
            j1 = np.searchsorted(lon_bins, x1, side="left")
            i0 = np.searchsorted(lat_bins, y0, side="right") - 1
            i1 = np.searchsorted(lat_bins, y1, side="left")

            j0 = max(j0, 0); i0 = max(i0, 0)
            j1 = min(j1, len(lon_bins)-1); i1 = min(i1, len(lat_bins)-1)

            for i in range(i0, i1):
                for j in range(j0, j1):
                    marked.add((i, j))

        for (i, j) in marked:
            grid[i, j] += 1  # conta 1 por frame

    grid = 100.0 * grid / n_total
    return pd.DataFrame(grid, index=lat_bins[:-1], columns=lon_bins[:-1])



def plot_map_occ(ax, grid):
    
    
  
    lat_lims = dict(min=-60, max=10, stp=10)
    lon_lims = dict(min=-100, max=-30, stp=15)
    
    gg.map_attrs(
        ax, None, 
        lat_lims = lat_lims, 
        lon_lims = lon_lims, 
        grid = False, 
        degress = None
        )
    
  
    
    img = ax.pcolormesh(
        grid.columns,
        grid.index,
        grid.values,
        vmin = 0, 
        vmax = 100,
        cmap="jet", 
    )
    return img



seasons = {
    "December": [12, 1, 2],
    "March": [3, 4, 5],
    "June": [6, 7, 8],
    "September": [9, 10, 11],
}

def plot_seasonal_occurrence_from_nl(nl, step=2.0,  ):
    
    fig, ax = plt.subplots(
        dpi=300, 
        ncols=4, 
        nrows=1, 
        figsize=(16, 10),
        subplot_kw={"projection": ccrs.PlateCarree()},
    )
    plt.subplots_adjust(wspace=0.02, hspace=0.12)

    axes = ax.flat 
    lat_min = np.round(nl['lat_min'].min())
    lon_min = np.round(nl['lon_min'].min())
    lon_max = np.round(nl['lon_max'].max())
    lat_max = np.round(nl['lat_max'].max())
    
    
    lon_bins = np.arange(lon_min, lon_max + step, step)
    lat_bins = np.arange(lat_min, lat_max + step, step)
    
    n_total = nl.index.unique().size

    for i, (name, months) in enumerate(seasons.items()):
        nl_season = nl.loc[nl.index.month.isin(months)]
        
        grid = occurrence_percent_grid(nl_season, lon_bins, lat_bins, n_total)
        
        img = plot_map_occ(axes[i], grid)

        l = b.chars()[i]
        axes[i].set_title(f"({l}) {name}", fontsize=28)

        if i != 0:
            axes[i].set(
                xticklabels=[], 
                xlabel="", 
                ylabel="", 
                yticklabels=[])
            
    anchor = [0.3, 0.78, 0.4, 0.025]
    cax = plt.axes(anchor)
    cbar = fig.colorbar(
        img, ax=ax.ravel().tolist(), 
        orientation = "horizontal",
        cax = cax,
        )

    cbar.set_label("Convection activity (\%)", fontsize=22)
    
    # fig.suptitle(str(year), y=0.98, fontsize=28)
    return fig

 
nl = b.load("nucleos_2012_2018")   

fig = plot_seasonal_occurrence_from_nl(nl, step = 4.0 )



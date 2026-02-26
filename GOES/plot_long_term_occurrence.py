import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import base as b
import GEO as gg

b.sci_format()
 

def occurrence_percent_grid(nl_season, step):
    df = nl_season.copy()
    
    lat_min = np.round(nl['lat_min'].min())
    lon_min = np.round(nl['lon_min'].min())
    lon_max = np.round(nl['lon_max'].max())
    lat_max = np.round(nl['lat_max'].max())
    
    
    lon_bins = np.arange(lon_min, lon_max + step, step)
    lat_bins = np.arange(lat_min, lat_max + step, step)
    
    df['year'] = df.index.year 
    # centro do núcleo
    df["lon"] = (df["lon_min"] + df["lon_max"]) / 2
    df["lat"] = (df["lat_min"] + df["lat_max"]) / 2

    df["lon_bin"] = pd.cut(
        df["lon"], lon_bins,
        labels=lon_bins[:-1], include_lowest=True)
    df["lat_bin"] = pd.cut(
        df["lat"], lat_bins,
        labels=lat_bins[:-1], include_lowest=True)

    df = df.groupby(['year', "lon_bin", "lat_bin"]).size().to_frame('count').reset_index()
          

 

    return  df



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

def plot_seasonal_occurrence_from_nl(nl, step=2.0):
    
    years = np.arange(2012, 2018)
    
    fig, ax = plt.subplots(
        dpi=300, 
        ncols=3, 
        nrows=2, 
        figsize = (12, 9),
        subplot_kw={"projection": ccrs.PlateCarree()},
    )
    plt.subplots_adjust(wspace=0.1, hspace=0.)

    axes = ax.flat 
    
    df = occurrence_percent_grid(nl, step = step)

    n_total = df['count'].max()
 
    
    for i, year in enumerate(years):
        nly = df.loc[df['year'] == year]
        
        nly['count']  = (nly['count']  / n_total) * 100

        grid = pd.pivot_table(
            nly, 
            columns = 'lon_bin', 
            index = 'lat_bin', 
            values = 'count'
            )
         
        img = plot_map_occ(axes[i], grid)

        l = b.chars()[i]
        axes[i].set_title(f"({l}) {year}", fontsize=28)

        if i != 3:
            axes[i].set(
                xticklabels=[], 
                xlabel="", 
                ylabel="", 
                yticklabels=[])
            
    anchor = [0.3, 0.8, 0.4, 0.025]
    # cax = plt.axes(anchor)
    # cbar = fig.colorbar(
    #     img, ax=ax.ravel().tolist(), 
    #     orientation = "horizontal",
    #     cax = cax,
    #     )

    # cbar.set_label("Convection activity (\%)", fontsize=22)
    
    # fig.suptitle(str(year), y=0.98, fontsize=28)
    return fig

 
# nl = b.load("nucleos_2012_2018")   

# fig = plot_seasonal_occurrence_from_nl(nl, step = 4.0 )


# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 22:26:16 2026

@author: Luiz
"""

def single_grid_mean(ax, df, step = 2):
    
    year = df.index[0].year
    lon_bins = make_regular_bins(df["lon"].min(), df["lon"].max(), step)
    lat_bins = make_regular_bins(df["lat"].min(), df["lat"].max(), step)
    
    
    grid = compute_seasonal_mean_grid(
            df, 
            lon_bins, 
            lat_bins, 
            value_col = "Ep_max"
            )
    

    grid = smooth_grid_if_needed(grid, sigma=1)
    img = plot_ep_grid_map(
        ax,
        grid,
        title= year,
        cmap="jet",
        vmin = 60,
        vmax = 100,
    )
    
    return img 

def plot_yearly_ep_map():
    
    fig, ax = plt.subplots(
        ncols = 3, 
        dpi = 300, 
        figsize = (14, 10), 
        nrows = 2,
        subplot_kw={"projection": ccrs.PlateCarree()}
        )
    
    plt.subplots_adjust(hspace = 0.1)
    ep_col = "Ep_mean"
    alt = 30
    
    for i, ax in enumerate(ax.flat):
        
        year = 2012 + i 
        
        df = gs.load_ep_data(
            year = year,
            alt = alt,
            ep_col = "Ep_mean"
        )
        
        img = single_grid_mean(ax, df, step = 2)
        
        if i != 3:
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.set_xlabel("")
            ax.set_ylabel("")
    
    
    cax = fig.add_axes([0.30, 0.95, 0.40, 0.02])
    
    cbar = fig.colorbar(
        img,
        cax = cax,
        orientation = "horizontal",
    )
    cbar.set_label(f"{ep_col} (J/kg) at {alt} km ", fontsize=20)
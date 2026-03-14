import GOES as gs
import matplotlib.pyplot as plt 
import datetime as dt 
import pandas as pd
import numpy as np 
from scipy.ndimage import gaussian_filter
import base as b 

def average_grid(df, values = 'mean_90_110', step = 2):
    lon_min = df['lon'].min()
    lon_max = df['lon'].max()
    lat_min = df['lat'].min()
    lat_max = df['lat'].max()
    
    
    lon_bins = np.arange(lon_min, lon_max + step, step)
    lat_bins = np.arange(lat_min, lat_max + step, step)
    
    df["lon_bin"] = pd.cut(
        df["lon"], lon_bins, 
        labels = lon_bins[:-1]
        )
    
    df["lat_bin"] = pd.cut(
        df["lat"], lat_bins, 
        labels=lat_bins[:-1]
        )
    
    counts = (
        df.groupby(["lon_bin", "lat_bin"])
          .mean() 
          .reset_index()
    )
     
    return pd.pivot_table(
        counts,
        index = "lat_bin",
        columns = "lon_bin",
        values = values 
    )

def gaussian_filter_nan(arr, sigma):
    arr = np.asarray(arr)

    mask = np.isfinite(arr)

    arr_filled = np.where(mask, arr, 0)

    smooth_data = gaussian_filter(arr_filled, sigma=sigma)
    smooth_mask = gaussian_filter(mask.astype(float), sigma=sigma)

    result = smooth_data / smooth_mask
    result[~mask] = np.nan

    return result

def smooth_grid(grid, sigma = 1.5):
    grid = grid.replace(np.nan, 0)
    
    return gaussian_filter(grid.values, sigma = sigma)

def colorbar(ax, img):
    cax = ax.inset_axes([1.1, 0, 0.05, 1])
     
    cb = plt.colorbar(
        img,  
        cax = cax, 
        )
    
    cb.set_label("Ep (J/kg)")
    
    return None



def plot_dialy_Ep_points(
        df, 
        step = 4,  
        values = 'mean_90_110'
    ):
    vmax = 90
    fig, ax = gs.map_defout(
        ncols = 4, 
        lon_max = -30,
        lon_min = -90,
        wspace = 0.4
        )
    
    grid = average_grid(df, values, step )
    
    img = ax[0].scatter(
        df['lon'], 
        df['lat'], 
        c = df[values],
        s = 100, 
        vmin = 0, 
        vmax = vmax,
        cmap = 'jet'
        )
    
    colorbar(ax[0], img)
    
    
    ax[1].pcolormesh(
        grid.columns, 
        grid.index,
        grid.values, 
        cmap = 'jet',
        vmin = 0, 
        vmax = vmax,
        )
    
    colorbar(ax[1], img)
    sigma = 1.
    
    method = 'linear'
    grid_fill = grid.interpolate(
            axis=1,# method = method
        ).interpolate(
            axis=0, #method = method 
            )
    
    ax[2].pcolormesh(
        grid_fill.columns, 
        grid_fill.index,
        grid_fill.values, 
        cmap = 'jet',
        vmin = 0, 
        vmax = vmax,
        )
    
    colorbar(ax[2], img)
    smooth = gaussian_filter(grid_fill.values, sigma=1.0)
    # smooth = gaussian_filter_nan(grid, sigma = sigma) 
    
    img = ax[-1].pcolormesh(
        grid_fill.columns, 
        grid_fill.index,
        smooth, 
        vmin = 0, 
        vmax = vmax,
        cmap = 'jet'
        )
    
    colorbar(ax[-1], img)
    
    ax[0].set( title = 'Raw data (SABER)')
    
    ax[1].set( title = f'Occurrence grid ({step}x{step})')
    ax[2].set( title = f'Grid Interpolated')
    ax[-1].set( title = f'Gaussian filter ($\sigma$ = {sigma})')
    dn = df.index[0]
    fig.suptitle(dn.strftime('%Y-%m-%d'), y = 0.7)
    
year = 2013 
path = f'D:\\database\\SABER\\ep\\{year}'
df = b.load(path)
 
df = df.loc[df.index.date == dt.date(2013, 1, 1)]

values = 'Ep_mean'
df = df.loc[df['alt'] == 110, ['lat', 'lon', values]]
plot_dialy_Ep_points(df, step = 4, values = values)


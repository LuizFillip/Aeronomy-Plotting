import pandas as pd
import numpy as np
import cartopy.crs as ccrs
import datetime as dt
import matplotlib.pyplot as plt
import base as b 
import GEO as gg 


b.config_labels(fontsize = 25)

def filter_data(df):
    for col in df.columns:
        if col < -60:
            df[col] = np.nan 


def load_tec(infile, values = True):

    df = pd.read_csv(
        infile, 
        delimiter = ';', 
        header = None
        ).replace(-1, np.nan)
    
    xmax, ymax = df.values.shape
    df.columns = np.arange(0, ymax)*0.5 - 90
    df.index = np.arange(0, xmax)*0.5 - 60
    
    if values:
        return df.columns, df.index, df.values
    else:
        return df

def plot_matrix(
        ax, infile, 
        step = 5, 
        vmax = 100,
        colorbar = True):
    
    lon, lat, values = load_tec(infile)
    
    ticks = np.arange(0, vmax, 15)
    levels = np.arange(0, vmax + step, step*0.5)
    
    img = ax.contourf(
        lon, lat, values, 
        levels = levels,
        cmap = 'rainbow'
        )
    
    if colorbar:
            
        b.colorbar(
            img, ax, ticks, 
            width = '5%',
            label = r'TEC ($10^{16} / m^2$)'
            )
    
    return img




def plot_tec_map(
        dn, 
        ax = None, 
        step = 1,
        vmax = 60, 
        colorbar = True
        ):
    
    if ax is None:
        fig, ax = plt.subplots(
             figsize = (10, 10), 
             dpi = 300, 
             subplot_kw = 
             {'projection': ccrs.PlateCarree()}
             )
    
    dn_min = b.closest_datetime(b.tec_dates(dn), dn)
    
    path = b.get_path(dn_min)
     
    img = plot_matrix(
        ax, path,
        step = step, 
        vmax = vmax, 
        colorbar = colorbar
        )
  
    
    gg.map_attrs(
        ax, dn.year, 
        grid = False,
        degress = None
        )
    
    gg.plot_rectangles_regions(ax, dn.year)
    lon, lat = gg.terminator2(dn, 18)
    
    ax.scatter(lon, lat, c = 'k', s = 5)
    
    ax.set(title = dn.strftime('%Y/%m/%d %Hh%M (UT)'))
    
    if ax is None:
        
        return fig
    else:
        if colorbar:
            return img
       


def main():
    
    dn = dt.datetime(2022, 1, 1, 1, 0)
    
    # df = load_tec(b.get_path(dn))
    
    fig = plot_tec_map(dn, ax = None)

# main()



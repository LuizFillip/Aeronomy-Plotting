import pandas as pd
import numpy as np
import cartopy.crs as ccrs
import datetime as dt
import matplotlib.pyplot as plt
import GEO as g
import base as b 
import plotting as pl


b.config_labels(fontsize = 25)


def load_tec(infile):

    df = pd.read_csv(
        infile, 
        delimiter = ';', 
        header = None
        ).replace(-1, np.nan)
    
    xmax, ymax = df.values.shape

    lat = np.arange(0, xmax)*0.5 - 60
    lon = np.arange(0, ymax)*0.5 - 90
         
    return lon, lat, df.values

def plot_contourf(ax, lon, lat, values, step = 5):
    
    v = np.arange(0, 70 + step, step*0.5)
    
    img = ax.contourf(
        lon, lat, values, 
        levels = v,
        cmap = 'rainbow'
        )
    
    b.colorbar(
        img, ax, v, 
        label = r'TEC ($10^{16} / m^2$)'
        )
    
    return img

def get_path(dn):
    infile = "D:\\database\\"
    fmt = 'TEC_%Y\\TEC_%Y_%m\\TECMAP_%Y%m%d_%H%M.txt'
    return infile +  dn.strftime(fmt)

def plot_tec_map(dn, ax = None):
    
    if ax is None:
        fig, ax = plt.subplots(
             figsize = (10, 10), 
             dpi = 300, 
             subplot_kw = 
             {'projection': ccrs.PlateCarree()}
             )
    
    lon, lat, vls =  load_tec(get_path(dn))
    
    plot_contourf(ax, lon, lat, vls)
    g.mag_equator(ax)
    g.map_features(ax)
    g.map_boundaries(ax)
    pl.plot_corners(ax, dn.year)
    
    term_lon, term_lat = g.terminator2(dn, 18)
    
    ax.scatter(term_lon, term_lat, s = 10)
    ax.set(title = dn.strftime('%Y/%m/%d %H:%M (UT)'))
    
    # if ax is None:
    #     return fig
    # else:
    #     return ax




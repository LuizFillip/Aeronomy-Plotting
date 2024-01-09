import os
import pandas as pd
import numpy as np
import cartopy.crs as ccrs
import datetime as dt
import matplotlib as mpl
import matplotlib.pyplot as plt
import GEO as g
import base as b 

b.config_labels(fontsize = 25)


def tec_fname(filename: str) -> dt.datetime:
    """Convert TEC filename (EMBRACE format) to dt"""
    args = filename.split('_')
    date = args[1][:4] + '-' + args[1][4:6]+ '-' +args[1][-2:] 
    time = args[-1].replace('.txt', '')
    time = time[:2] + ':' + time[2:]
    
    return dt.datetime.strptime(
        date + ' ' + time, 
        "%Y-%m-%d %H:%M"
        )

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
    
    v = np.arange(0, 80 + step, step*0.5)
    
    img = ax.contourf(lon, lat, values, levels = v,
                      cmap = 'rainbow')
    
 
    b.colorbar(img, ax, v, 
            label = r'TEC ($10^{16} / m^2$)')
    
    return img


def plot_tec_map(infile, fontsize = 25):

    fig, ax = plt.subplots(
         figsize = (10, 10), 
         dpi = 300, 
         subplot_kw = 
         {'projection': ccrs.PlateCarree()}
         )
    
    lon, lat, vls =  load_tec(infile)
    
    plot_contourf(ax, lon, lat, vls)
    g.mag_equator(ax)
    g.map_features(ax)
    g.map_boundaries(ax)
    
    fname = os.path.split(infile)[-1]
    
    
    ax.set(title = tec_fname(
        fname).strftime('%Y/%m/%d %H:%M'))
    
    return fig

def get_path(dn):
    infile = "D:\\database\\"
    fmt = 'TEC_%Y\\TEC_%Y_%m\\TECMAP_%Y%m%d_%H%M.txt'
    return infile +  dn.strftime(fmt)

dn = dt.datetime(2013, 12, 25, 23)

fig = plot_tec_map(get_path(dn), fontsize = 40)
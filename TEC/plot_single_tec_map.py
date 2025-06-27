import plotting as pl 
import numpy as np
import cartopy.crs as ccrs
import datetime as dt
import matplotlib.pyplot as plt
import base as b 
import GEO as gg 


def filter_data(df):
    for col in df.columns:
        if col < -60:
            df[col] = np.nan 
    return df


def plot_matrix(
        ax, 
        infile, 
        vmax = 30,
        colorbar = True,
        vertical_cbar = True
        ):
    
    lon, lat, values = pl.load_tec(infile)
    
    levels = np.linspace(0, vmax, 16)
    
    values = np.where(values > vmax, vmax, values)
    
    img = ax.contourf(
        lon, lat, 
        values, 
        levels = levels,
        cmap = 'jet'
        )
    step = vmax / 5
    
    ticks = np.arange(0, vmax + step, step).round(0)
    
    if colorbar:
       
        if vertical_cbar:
            b.colorbar(
                    img, 
                    ax, 
                    ticks, 
                    label = 'TECU ($10^{16}/m^2$)', 
                    height = "100%", 
                    width = "10%",
                    orientation = "vertical", 
                    anchor = (.25, 0., 1, 1)
                    )
        else:
            b.colorbar(
                    img, 
                    ax, 
                    ticks, 
                    label = 'TECU ($10^{16}/m^2$)', 
                    height = '10%' , 
                    width = "80%",
                    orientation = "horizontal", 
                    anchor = (-0.26, 0.7, 1.26, 0.55)
                    )
            
    
    return img

    
  

def plot_tec_map(
        dn, 
        ax = None, 
        vmax = 60, 
        colorbar = True, 
        boxes = False,
        title = False,
        invert_axis = False,
        root = 'E:\\',
        vertical_cbar = True
        ):
    
    if ax is None:
        fig, ax = plt.subplots(
             figsize = (10, 10), 
             dpi = 300, 
             subplot_kw = 
             {'projection': ccrs.PlateCarree()}
             )
        ax.set(title = dn.strftime('%B %d, %Y %Hh%M (UT)'))
    
    dn_min = b.closest_datetime(b.tec_dates(dn, root = root), dn)
    
    path = b.get_path(dn_min, root = root)
     
    plot_matrix(
        ax, path,
        vmax = vmax, 
        colorbar = colorbar,
        vertical_cbar = vertical_cbar
        )

    gg.map_attrs(
        ax, dn.year, 
        grid = False,
        degress = None
        )
    
    if invert_axis:
        ax.tick_params(
            top = True,
            right = True,
            left = False,
            bottom = False,
            labelright = True,
            labelleft = False,
            labeltop = True, 
            labelbottom = False, 
            
            )
        ax.yaxis.set_label_position("right")
        ax.xaxis.set_label_position("top")
        

    if boxes:
        gg.plot_rectangles_regions(ax, dn.year)
        
    lon, lat = gg.terminator2(dn, 18)
    
    ax.scatter(lon, lat, c = 'k', s = 5)
    
    # return fig
        

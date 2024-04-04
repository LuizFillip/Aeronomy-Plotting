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
        colorbar = True
        ):
    
    lon, lat, values = load_tec(infile)
    
    levels = np.arange(0, vmax + step, step*0.5)
    levels = np.linspace(0, vmax + step, 16)
    img = ax.contourf(
        lon, lat, 
        values, 
        levels = levels,
        cmap = 'jet'
        )
    
    # if colorbar:
        # ticks = np.arange(0, vmax, 15)
        # b.colorbar(
        #     img, ax, ticks, 
        #     width = '5%',
        #     label = r'TEC ($10^{16} / m^2$)'
        #     )
        
       
    
    return img

    
  

def plot_tec_map(
        dn, 
        ax = None, 
        step = 1,
        vmax = 60, 
        colorbar = True, 
        boxes = False,
        title = False,
        site = 'SAKK', 
        invert_axis = True
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
    
    ticks = np.arange(0, vmax + 2, 2)
    b.colorbar(
            img, 
            ax, 
            ticks, 
            label = 'TECU ($16^{16}/m^2$)', 
            height = "100%", 
            width = "3%",
            orientation = "vertical", 
            anchor = (.25, 0., 1, 1)
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
    
    # ax.set(title = 'Longitude (°)', xlabel = '')
    
    
    if boxes:
        gg.plot_rectangles_regions(ax, dn.year)
        
    lon, lat = gg.terminator2(dn, 18)
    
    ax.scatter(lon, lat, c = 'k', s = 5)
    
        
    
    
    if ax is None:
        
        return fig
    else:
        # ax.set(title = dn.strftime('%Y/%m/%d %Hh%M (UT)'))
        return img
      
       


def main():
    
    dn = dt.datetime(2016, 10, 4, 2, 20)
    
    # df = load_tec(b.get_path(dn))
    
    fig = plot_tec_map(dn, ax = None, vmax = 25, invert_axis=False)

# main()



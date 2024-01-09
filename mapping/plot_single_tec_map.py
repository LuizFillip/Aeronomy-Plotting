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

def load_and_plot(ax, infile, step = 5):

    df = pd.read_csv(
        infile, 
        delimiter = ';', 
        header = None
        ).replace(-1, np.nan)
    
    
    xmax, ymax = df.values.shape

    lat = np.arange(0, xmax)*0.5 - 60
    lon = np.arange(0, ymax)*0.5 - 90
    
    v = np.arange(0, 80 + step, step*0.5)
    img = ax.contourf(lon, lat, df.values, levels = v,
                      cmap = 'rainbow')
    
 
    fname = os.path.split(infile)[-1]
    ax.set(title = tec_fname(fname).strftime('%d/%m %H:%M'))
    
    return img
    
def plot_colorbar(
        fig,
        rainbow = "rainbow",
        fontsize = 40
        ):
    
    norm = mpl.colors.Normalize(
        vmin = 0, vmax=80
        )
   
    cax = plt.axes([0.2, 1.001, 0.6, 0.02])
         
    cb = fig.colorbar(
        mpl.cm.ScalarMappable(
            norm = norm, 
            cmap = rainbow
            ),
        ticks = np.arange(0, 80, 10),
        cax = cax, 
        orientation = "horizontal", 
        )
    cb.set_label(r'TEC ($10^{16} / m^2$)', fontsize = fontsize)
    


    
    


def plot_tec_map(infile, fontsize = 40):

    fig, ax = plt.subplots(
         figsize = (20, 15), 
         dpi = 300, 
         ncols = 5, 
         nrows = 3,
         subplot_kw = 
         {'projection': ccrs.PlateCarree()}
         )
    
    plt.subplots_adjust(wspace = 0.05, hspace=0.25)
        
    delta = dt.timedelta(hours = 4)
    
    vlats = dict(min = -30, max = 10, stp = 5)
    vlons = dict(min = -60, max = -30, stp = 5) 
    
    for row, day in enumerate([16, 17, 18]):
        dn = dt.datetime(2013, 3, day, 22, 0)
        times = pd.date_range(dn, dn + delta, freq = "1H")
        
        for col, time in enumerate(times):
            filename = time.strftime("TECMAP_%Y%m%d_%H%M.txt")
    
            load_and_plot(ax[row, col], infile + filename, step = 5)
            g.mag_equator(ax[row, col])
            g.map_features(ax[row, col])
    
            
            ax[row, col].set(
                ylim = [vlats['min'], vlats['max']], 
                xlim = [vlons['min'], vlons['max']]
                )
            
        ax[row, 0].set(
            xticks = np.arange(
                vlons['min'], vlons['max'] + 10, 10
                ), 
            yticks = np.arange(
                vlats['min'], vlats['max'] + 10, 10
                )
            )
    
   
    plot_colorbar(
            fig
            )
    
    fig.text(.07, 0.43, "Latitude (°)", 
             rotation = "vertical", fontsize = fontsize)
    fig.text(.43, 0.07, "Longitude (°)", 
             fontsize = fontsize)
                
    return fig
# infile = "D:\\database\\TEC_2013\\TEC_2013_03\\"
# fig = plot_tec_map(infile)     
# fig.savefig("digisonde/src/figures/tec_maps.png")
# plt.show()
import os
import numpy as np
import cartopy.crs as ccrs
import datetime as dt
import matplotlib.pyplot as plt
import base as b 
import GEO as gg 
import PlasmaBubbles as pb 

b.config_labels(fontsize = 50)
# for hour in [22, 0, 2, 4, 6]:
    
def plot_ipp_over_map(hour):
    

    fig, ax = plt.subplots(
         figsize = (12,12), 
         dpi = 300, 
         subplot_kw = 
         {'projection': ccrs.PlateCarree()}
         )


    dn = dt.datetime(2021, 1, 1, hour)
    
    path = 'E:\\database\\GNSS\\001\\'
    
    for file in os.listdir(path):
        
        ds = pb.load_filter(path + file)
    
        df = b.sel_times(ds, dn, hours = 0.1)
        
        img = ax.scatter(
            df['lon'], 
            df['lat'], 
            c = df['roti'], 
            cmap = 'jet',
            s = 10, 
            vmax = 1, 
            vmin = 0)
        
        gg.map_attrs(
             ax, dn.year, 
             grid = False,
             degress = None
             )
        
        lon, lat = gg.terminator2(dn, 18)
         
        ax.scatter(lon, lat, c = 'k', s = 5)
        
        
        gg.plot_square_area(
                ax, 
                lat_min = -10, 
                lon_min = -50)
    
    ax.set(title = dn.strftime('24-25/12/2013 %Hh%M (UT)'))
    
    
    ticks = np.arange(0, 1, 0.1)
    b.colorbar(
             img, 
             ax, 
             ticks, 
              label = 'ROTI (TECU/min)', 
             orientation = "vertical", 
              anchor = (.1, 0., 1, 1)
             )
    
    return fig
  
    
fig = plot_ipp_over_map(hour)


# fig.savefig(dn.strftime('%H'), dpi = 500)
    
    
FigureName = 'cicle_slip_demo'


# fig.savefig(
#       b.LATEX(FigureName, folder = 'timeseries'),
#       dpi = 400
#       )
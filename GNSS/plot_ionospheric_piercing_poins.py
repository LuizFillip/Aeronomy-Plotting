import os
import numpy as np
import cartopy.crs as ccrs
import datetime as dt
import matplotlib.pyplot as plt
import base as b 
import GEO as gg 
import PlasmaBubbles as pb 
import GNSS as gs 
b.config_labels(fontsize = 50)

    
def plot_ipp_over_map(dn):
    

    fig, ax = plt.subplots(
         figsize = (12,12), 
         dpi = 300, 
         subplot_kw = 
         {'projection': ccrs.PlateCarree()}
         )


    lat_lims = dict(min = -30, max = 20, stp = 10)
    lon_lims = dict(min = -80, max = -30, stp = 10) 

    doy = gs.doy_from_date(dn)
    path = gs.paths(dn.year, doy, root = 'E:\\').fn_roti()

    ds = pb.load_filter(path, remove_noise = False)

    df = b.sel_times(ds, dn, hours = 0.4)
    
    img = ax.scatter(
        df['lon'], 
        df['lat'], 
        c = df['roti'], 
        cmap = 'jet',
        s = 30, 
        vmax = 5, 
        vmin = 0)
    
    gg.map_attrs(
       
         ax, dn.year, 
         grid = False,
         lat_lims = lat_lims,
         lon_lims = lon_lims,
         degress = None
         )
    
    lon, lat = gg.terminator2(dn, 18)
     
    ax.scatter(lon, lat, c = 'k', s = 5)
    
    
    gg.plot_square_area(
            ax, 
            lat_max = 8,
            lat_min = -6, 
            lon_min = -50)

    ax.set(title = dn.strftime('24-25/12/2013 %Hh%M (UT)'))
    
    
    ticks = np.arange(0, 6, 1)
    b.colorbar(
             img, 
             ax, 
             ticks, 
             label = 'ROTI (TECU/min)', 
             orientation = "vertical", 
              anchor = (.1, 0., 1, 1)
             )
    
    return fig
  
hour = 22    
import pandas as pd 
start = dt.datetime(2013, 12, 24, 22)

times = pd.date_range(start, freq = '2H', periods = 5)

for dn in times:
    fig = plot_ipp_over_map(dn)
    FIgureName = dn.strftime('%d%H%M')
    
    fig.savefig(FIgureName)


# fig.savefig(dn.strftime('%H'), dpi = 500)
    
    
# FigureName = 'cicle_slip_demo'
# path = gs.paths(2013, 358, root = 'E:\\').fn_roti()
# ds = pb.load_filter(path, remove_noise = False)

# ds['roti'].plot(ylim = [0, 5])

# times 
import GEO as gg 
from intersect import intersection
import numpy as np
from FluxTube import Apex
import base as b 
import matplotlib.pyplot as plt 
import cartopy.crs as ccrs

def plot_ranges_for_each_apex(
         x, y,
         ax,
         amin = 200, 
         amax = 500, 
         step = 100, 
         base = 150,
         set_hemis = "south"
         ):
 
     heights = np.arange(amin, amax + step, step)[::-1]
          
     for alt in heights:
         
         mlat = Apex(alt).apex_lat_base(base = base)
         
         rlat = np.degrees(mlat)
         
         x1, y1 = gg.limit_hemisphere(
                 x, y, rlat, 
                 hemisphere = set_hemis
                 )
         
         ax.plot(x1, y1, "--", 
                label = f"{alt} km", 
                lw = 2)
         
      
def plot_site_and_closest_meridian(
        ax, 
        site = "saa"
        ):
      
      fig, ax = plt.subplots(
          dpi = 300,
          figsize = (8, 8),
          subplot_kw = 
              {
              'projection': ccrs.PlateCarree()
              }
          )

      path = 'database/20130101.txt'

      df = b.load(path)

      dn = df.index.unique()[0]
      
      gg.map_features(ax)

      ds = df.loc[(df.index == dn) & 
                  (df['apex'] == 300)]
      
      
      print(len(ds))
      lat = gg.limits(
          min = -25, 
          max = 15, 
          stp = 10
          )
      lon = gg.limits(
          min = -85, 
          max = -30, 
          stp = 10
          )    

      gg.map_boundaries(ax, lon, lat)


      img = ax.scatter(
          ds['glon'], 
          ds['glat'], 
          c = ds['zon']
          )


      return 





# path = 'database/20130101.txt'

# df = b.load(path)

# dn = df.index.unique()[0]

# ds = df.loc[(df.index == dn) & 
#             (df['apex'] == 300)]


# ds['glat'], ds['glon']

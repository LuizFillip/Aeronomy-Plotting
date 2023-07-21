from GEO import quick_map, sites, load_equator
from intersect import intersection
import numpy as np
from FluxTube import Apex

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
         
         x1, y1 = limit_hemisphere(
                 x, y, rlat, 
                 hemisphere = set_hemis
                 )
         
         ax.plot(x1, y1, "--", 
                label = f"{alt} km", 
                lw = 2)
         
      
def plot_site_and_closest_meridian(
        ax, 
        site = "saa"):
      
      glat, glon = sites[site]["coords"]
      name = sites[site]["name"]
      
      ax.scatter(
          glon, glat, 
          s = 100, 
          label = name, 
          marker = "^"
          )
      
      x, y = find_closest_meridian(glon, glat)
      
      eq = load_equator()
      
      nx, ny = intersection(
          eq[:, 0], 
          eq[:, 1], 
          x, y
          )
      
      ax.scatter(nx, ny, s = 100, c = "r",
                 label = "intersecção")
      
      ax.plot(x, y, lw = 2, 
              color = "salmon", 
              label = "meridiano magnético")
      
      return x, y




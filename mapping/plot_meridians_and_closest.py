import GEO as gg 
import matplotlib.pyplot as plt 
import cartopy.crs as ccrs
import datetime as dt
         
      
def plot_meridians_and_closest(dn):
      
      fig, ax = plt.subplots(
          dpi = 300,
          figsize = (8, 8),
          subplot_kw = 
              {'projection': ccrs.PlateCarree()}
          )

  
      lat_lims = dict(min = -30, max = 30, stp = 10)
      lon_lims = dict(min = -70, max = -30, stp = 10) 

      gg.map_attrs(
          ax, year = 2013, 
          lon_lims = lon_lims, 
          lat_lims = lat_lims,
          grid = False,
          degress = None)

      mer = gg.meridians(dn, delta = 5)
      
      glat, glon = gg.sites['saa']['coords']
      
      meridian = mer.range_meridians()
      
      for num in range(meridian.shape[0]):
          
          x, y = meridian[num][0], meridian[num][1]
          
          ax.plot(x, y, lw = 1, color = 'k')
          
      x, y = mer.closest_from_site(glon, glat)
      
      nx, ny = gg.intersec_with_equator(x, y, dn.year)
      
      ax.scatter(
          nx, ny, 
          marker = '^', 
          c = 'r', 
          s = 150,
          label = 'intersecção com equador'
          )
      
      ax.scatter(
          glon, glat, 
          marker = 's',
          s = 150,
          c = 'r',
          label = 'São Luís'
          )
      
      
      ax.plot(x, y, color = 'r', lw = 2)
      rlat = 12.236
      
      xe, ye = gg.limit_hemisphere(
              x, y, nx, ny, rlat, 
              hemisphere = 'both'
              )
      
      ax.plot(xe, ye, 'k', lw = 3,
              linestyle = '--')
      return fig 


dn = dt.datetime(2013, 12, 24)

fig = plot_meridians_and_closest(dn)
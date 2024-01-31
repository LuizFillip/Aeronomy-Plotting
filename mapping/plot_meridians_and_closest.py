import GEO as gg 
import matplotlib.pyplot as plt 
import cartopy.crs as ccrs
import datetime as dt
import base as b 

b.config_labels(fontsize = 35)
      
def plot_meridians_and_closest(dn):
      
      fig, ax = plt.subplots(
          dpi = 300,
          figsize = (12, 12),
          subplot_kw = 
              {'projection': ccrs.PlateCarree()}
          )

  
      lat_lims = dict(min = -30, 
                      max = 30, 
                      stp = 10)
      lon_lims = dict(min = -70, 
                      max = -30, 
                      stp = 10) 

      gg.map_attrs(
          ax, year = 2013, 
          lon_lims = lon_lims, 
          lat_lims = lat_lims,
          grid = False,
          degress = None)

      mer = gg.meridians(dn, delta = 5)
      
      glat, glon = gg.sites['saa']['coords']
      
      meridian = mer.range_meridians()
      
      # for num in range(meridian.shape[0]):
          
      #     x, y = meridian[num][0], meridian[num][1]
          
      #     ax.plot(x, y, lw = 1, color = 'k')
          
      x, y = mer.closest_from_site(glon, glat)
      
      nx, ny = gg.intersec_with_equator(x, y, dn.year)
      
      ax.scatter(
          nx, ny, 
          marker = '^', 
          c = 'r', 
          s = 150,
          label = 'Intersecção com equador'
          )
      print(nx, ny)
      
      ax.scatter(
          glon, glat, 
          marker = '^',
          s = 200,
          c = 'b',
          label = 'São Luís'
          )
      
      
      ax.plot(x, y, color = 'k', lw = 2, 
              label = 'Meridiano magnético')
      rlat = 12.236
      
      
      ax.legend(
          loc = 'upper center', 
        #  bbox_to_anchor = (0.5, 1.3)
          )
      
      # xe, ye = gg.limit_hemisphere(
      #         x, y, nx, ny, rlat, 
      #         hemisphere = 'both'
      #         )
      
      # ax.plot(xe, ye, 'k', lw = 3,
      #         linestyle = '--')
      return fig 


dn = dt.datetime(2013, 12, 24)

fig = plot_meridians_and_closest(dn)
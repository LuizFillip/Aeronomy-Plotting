import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import GEO as g
import base as b 
import datetime as dt
import PlasmaBubbles as pb

b.config_labels()

def plot_terminator_lines(
        ax, 
        dn,
        angle = 18,
        glat = -7
        ):
 
      for long in pb.longitudes():
          long = long + 10
                            
          dusk = pb.dusk_time(dn, long)
         
          lon, lat = g.terminator(dusk, angle)
          
          line, = ax.plot(
              lon, 
              lat, 
              lw = 2, 
              linestyle = '--'
              )
        
          ax.axhline(glat, lw = 1.5, linestyle = '--')
        
          time = dusk.strftime('%H:%M')
        
          ax.text(long, 11, time, 
                transform = ax.transData,
                color = line.get_color()
                )
        
          ax.axvline(
              long,
            color = line.get_color()
            )
          
      return ax
      
     
def plot_terminators_in_each_sector(
        dn
        ):
    
    fig, axs = plt.subplots(
        dpi = 300,
        figsize = (10, 10),
        subplot_kw={
            'projection': ccrs.PlateCarree()
            }
        )

    g.map_features(axs)

    lat = g.limits(
        min = -40.0, 
        max = 10, 
        stp = 10
        )
    lon = g.limits(
        min = -80, 
        max = -20, 
        stp = 10
        )    

    g.map_boundaries(axs, lon, lat)

    plot_terminator_lines(axs, dn)
        
    g.mag_equator(
            axs, 
            year = dn.year, 
            degress = None
            )
    
    # fig.suptitle(
    #     dn.strftime('%d/%m/%Y'), 
    #     y = 0.85
    #     )

    return 
    
dn = dt.datetime(2022, 1, 1, 0)
d = plot_terminators_in_each_sector(dn)




import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import GEO as g

def plot_equators_meridians(
        years = [2013, 2014, 2015],
        site = 'saa'
        ):

    fig, ax = plt.subplots(
        figsize = (8, 8), 
        dpi = 300, 
        subplot_kw = 
        {'projection': ccrs.PlateCarree()}
        )
    
    lat_lims = dict(min = -25, max = 15, stp = 5)
    lon_lims = dict(min = -80, max = -35, stp = 5) 
    
    g.map_features(ax)
    
    lat = g.limits(**lat_lims)
    lon = g.limits(**lon_lims)    
    
    g.map_boundaries(ax, lon, lat)
    
    
    colors = ['r', 'b', 'g']
    for i, year in enumerate(years):
        g.mag_equator(
            ax, 
            year = year, 
            color = colors[i]
            )
        
        nx, ny, x, y = g.load_meridian(year)
        
        ax.plot(x, y, lw = 2)
        
    glat, glon = g.sites['saa']['coords']
    
    ax.scatter(glon, glat, 
               s = 200, 
               label = 'São Luis'
               )
    
    ax.legend(years, loc = 'upper right')
    
# plot_equators_meridians([2013])
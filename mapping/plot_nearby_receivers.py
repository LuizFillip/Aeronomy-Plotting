import GEO as gg
import cartopy.crs as ccrs



args = dict( 
    s = 40, 
    marker = '^',
    color = 'k', 
    transform = ccrs.PlateCarree()
    )


def plot_receivers_coords(
        axs, 
        year, 
        distance = 5
        ):
    

    sites = gg.load_coords(year)
    
    out = []
 
    
    for name, key in sites.items():
        lon, lat, alt = tuple(key)
        
        if distance is not None:
            min_d = gg.distance_from_equator(
                    lon, 
                    lat, 
                    year = year
                    )
                    
            if min_d < distance:
            
                axs.scatter(
                    lon, lat, **args
                    )
            
                out.append(name)
        
    return out
    

            

def plot_sites_and_receivers(
        year = 2021,
        distance = 6
        ):
    
    lat_lims = dict(
        min = -15, 
        max = 10, 
        stp = 5
        )

    lon_lims = dict(
        min = -90,
        max = -30, 
        stp = 10
        )    

    fig, ax = gg.quick_map(
        lat_lims = lat_lims, 
        lon_lims = lon_lims, 
        figsize = (9, 9), 
        year = year, 
        degress = distance
        )
    
    
    r = plot_receivers_coords(
        ax, year, 
        distance
        )
    
    # glat, glon = gg.sites['saa']['coords']
    # gg.circle_range(ax, glon, glat, radius = 500)
    
    return r

# receivers = plot_sites_and_receivers()
# 
# len(receivers)
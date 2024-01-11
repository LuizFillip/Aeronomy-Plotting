import cartopy.crs as ccrs
import GEO as gg
import matplotlib.pyplot as plt



def plot_corners(
        ax,
        year,
        radius = 10,
        label = False,
        center = True
        ):
    
    coords = gg.corner_coords(
            year, 
            radius, 
            angle = 45
            )

    x_limits, y_limits = coords[0][::-1], coords[1][::-1]
    
    out = {}

    for i in range(len(x_limits)):
        index = i + 1
        
        xlim, ylim = x_limits[i], y_limits[i]
        
        ax.plot(
            xlim, ylim,
            color = 'black', 
            linewidth = 2, 
            transform = ccrs.PlateCarree() 
            )
        
        clon = sum(list(set(xlim))) / 2
        clat = sum(list(set(ylim))) / 2
        
        if center:
            ax.scatter(clon, clat, c = 'k', s = 100)
        
                
        if label:
            

            ax.text(clon, max(ylim) + 1, index, 
                    transform = ax.transData)
        
        x_values = sorted(list(set(xlim)))
        y_values = sorted(list(set(ylim)))
        
        out[index] = (x_values, y_values)
    
    return out

def plot_regions_over_map(year = 2013):
    
    fig, ax = plt.subplots(
        dpi = 300,
        sharex = True, 
        figsize = (10,10),
        subplot_kw = {'projection': ccrs.PlateCarree()}
    )
    
    gg.map_attrs(ax, year)
    
    corners = plot_corners(
            ax,
            year,
            radius = 10,
            label = False 
            )
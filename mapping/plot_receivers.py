import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import GEO.mapping as m
import setup as s
import json 
from build import paths as p



def plot_mapping_with_sites_locations():
    
    fig, axs = plt.subplots(
        figsize = (10, 10),
        subplot_kw={'projection': ccrs.PlateCarree()}
        )

    s.config_labels()

    m.map_features(axs)

    lat = m.limits(min = -40.0, max = 10, stp = 10)
    lon = m.limits(min = -80, max = -30, stp = 10)    

    m.map_boundaries(axs, lon, lat)
    
    infile = p("GEO").get_files_in_dir("sites")
    sites = json.load(open(infile))
    
    for name, key in sites.items():
        lat = key["lat"]
        lon = key["lon"]
        
        axs.scatter(lon, lat, s = 20, color = 'red', 
                transform = ccrs.PlateCarree(), label = name)
        
        axs.annotate(name, xy=(lon, lat),  xycoords='data',
                xytext=(lon - 100, lat + 10), textcoords='offset points',
                arrowprops=dict(facecolor='black', arrowstyle="->"), 
                horizontalalignment='right', verticalalignment='top',
                transform = ccrs.Geodetic())
    
    axs.axhline(0, color= 'k', linestyle = '--', lw =1)
    
    


plot_mapping_with_sites_locations()


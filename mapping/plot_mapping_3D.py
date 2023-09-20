from matplotlib.collections import LineCollection
from cartopy.mpl.patch import geos_to_path
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import itertools
import matplotlib.pyplot as plt
import numpy as np
import base as s
import GEO as gg
from FluxTube import Apex


def mapping_3D(fig, lat_lim = 30):
    
    ax = fig.add_subplot(111, projection = '3d')
     
    ax.xaxis.set_pane_color((1.0, 0.0, 1.0, .0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, .0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    
    ax.grid(False)
    
    tmp_planes = ax.zaxis._PLANES 
    ax.zaxis._PLANES = (
        tmp_planes[2], tmp_planes[3], 
        tmp_planes[0], tmp_planes[1], 
        tmp_planes[4], tmp_planes[5]
        )
    
    ax.set(xlim = [-180, 180], 
           ylim = [-lat_lim, lat_lim],
           zlim = [0, 500]
           )
   
    ax.view_init(azim = 230, elev = 50)
    
    target_projection = ccrs.PlateCarree()
    
    feature = cfeature.NaturalEarthFeature(
        'physical', 'coastline', '110m')
    

    filtered_geoms = [
        geom for geom in feature.geometries() 
        if -lat_lim <= geom.centroid.y <= lat_lim]
    geoms = [target_projection.project_geometry(
        geom, feature.crs)
             for geom in filtered_geoms]

    paths = list(itertools.chain.from_iterable(
        geos_to_path(geom) 
        for geom in geoms))

    
    segments = []
    
    for path in paths:
        vertices = [vertex for vertex, _ in 
                    path.iter_segments()]
        vertices = np.asarray(vertices)
                  
        segments.append(vertices)
    
    lc = LineCollection(
        segments, 
        lw = 0.5, 
        color ='black'
        )
    
    s.config_labels()
    ax.add_collection3d(lc)
    return ax

def plot_meridians_apex_3D(
        ax,
        year = 2015, 
        apex = 300, 
        site = 'saa'
        ):
            
    apx = Apex(apex)
    
    nx, ny, x, y  = gg.load_meridian(
        year, site = site
        )
    
    mlat = apx.apex_lat_base(base = 0)

    rlat = np.degrees(mlat)
    
    x1, y1 = gg.limit_hemisphere(
            x, y, nx, ny, rlat, 
            hemisphere = 'both'
            )
    
    heights = apx.apex_range(
        points = len(x1),
        base = 0)
    

    ax.plot(x1, y1, 
            np.zeros(len(x1)), 
            lw = 2, 
            color = "k", 
            linestyle = '--'
            )
    
    
    ax.plot(x1, y1, heights, 
            color = "k",
            lw = 2, 
            )
    
    
    glat, glon = gg.sites[site]['coords']
    name = gg.sites[site]['name']
    
    ax.plot(glon, glat, 0,
            marker = "^", 
            color = "red", 
            label = name
            )
    
        
def plot_meridians_and_site(
        year = 2013,
        lat_lim = 60
        ):
    
    fig = plt.figure(
        figsize = (12, 14),
        dpi = 300, 
        )
    
    ax = mapping_3D(fig, lat_lim = lat_lim)
    
    gg.mag_equator(ax)
    
    ax.set(
        ylabel = "Latitude (°)", 
        xlabel = "Longitude (°)", 
        zlabel = "Apex height (km)", 
        xticks = np.arange(-180, 200, 45), 
        yticks = np.arange(-lat_lim, lat_lim, 15), 
        )
    
    
    plot_meridians_apex_3D(
            ax,
            year, 
            apex = 300, 
            site = 'saa'
            )
    
    plot_meridians_apex_3D(
            ax,
            year, 
            apex = 300, 
            site = 'jic'
            )


from matplotlib.collections import LineCollection
from cartopy.mpl.patch import geos_to_path
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import itertools
import matplotlib.pyplot as plt
import numpy as np
import settings as s
from GEO.src.mapping import mag_equator
from GEO.src.core import compute_meridian, coords
from FluxTube.src.mag import Apex
from utils import save_plot


def mapping_3D(fig):
    
    ax = fig.add_subplot(111, projection = '3d')
     
    ax.xaxis.set_pane_color((1.0, 0.0, 1.0, .0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, .0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    
    ax.grid(False)
    
    tmp_planes = ax.zaxis._PLANES 
    ax.zaxis._PLANES = ( tmp_planes[2], tmp_planes[3], 
                        tmp_planes[0], tmp_planes[1], 
                        tmp_planes[4], tmp_planes[5])
    
    ax.set(xlim = [-180, 180], 
           ylim = [-90, 90],
           zlim = [0, 300]
           )
   
    ax.view_init(azim = -20, elev = 50)
    
    target_projection = ccrs.PlateCarree()
    
    feature = cfeature.NaturalEarthFeature(
        'physical', 'coastline', '110m')
    
    
    geoms = [target_projection.project_geometry(
        geom, feature.crs) for geom in feature.geometries()]
    
    paths = list(itertools.chain.from_iterable(
        geos_to_path(geom) for geom in geoms))
    
    segments = []
    
    for path in paths:
        vertices = [vertex for vertex, _ in 
                    path.iter_segments()]
        vertices = np.asarray(vertices)
                  
        segments.append(vertices)
    
    lc = LineCollection(
        segments, lw = 0.5, color='black'
        )
    
    s.config_labels()
    ax.add_collection3d(lc)
    return ax

def plot_mapping_3D():
        
    fig = plt.figure(
        figsize = (12, 10),
        dpi = 400, 
        )
    
    ax = mapping_3D(fig)
    
    mag_equator(ax)
    
    start_lon = -50
    
    apx = Apex(300)
    max_lat = np.degrees(apx.apex_lat_base(base = 0))
    
    xx, yy  = compute_meridian(
            lon = start_lon, 
            max_lat = max_lat,
            alt = 0, 
            year = 2013
            )
    
    ax.plot(xx, yy, np.zeros(len(xx)), lw = 2, 
            color = "b", label = "Meridiano magnético")
    heights = apx.apex_range(step = len(xx), base = 0)
    
    ax.plot(xx, yy, heights, color = "k", lw = 2, 
            label = 'Linha de campo')
    
    
    ax.set(ylabel = "Latitude (°)", 
           xlabel = "Longitude (°)", 
           zlabel = "Altura de apex (km)", 
           xticks = np.arange(-180, 200, 45), 
           yticks = np.arange(-90, 100, 30))
    
    glon, glat = coords["saa"][::-1]
    
    ax.plot(glon, glat, 0,
            marker = "^", 
            color = "red", 
            label = "São luis")
    
    
    ax.legend(loc = "upper center")
    
    plt.show()
    
    return fig

save_plot(plot_mapping_3D)

# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 18:52:46 2026

@author: Luiz
"""

def empty_elipses():
    import matplotlib.pyplot as plt
    from matplotlib.patches import Ellipse
     
     
    fig, ax = plt.subplots(
        # ncols = 2,
        dpi = 300,  
        )
    
    dn = dt.datetime(2013, 1, 1)
    
    fn = gs.get_path_by_dn(dn)
    lon, lat, temp = gs.read_gzbin(fn)
    
    nl = gs.find_nucleos(
         lon,
         lat,
         temp,
         dn=None,
         temp_threshold=-50,
     )
     
    row = nl.loc[nl['area']> 100].iloc[0]
     
    lon0, lon1 = row["lon_min"], row["lon_max"]
    lat0, lat1 = row["lat_min"], row["lat_max"]
     
    
    x0, x1 = sorted([lon0, lon1])
    y0, y1 = sorted([lat0, lat1])
    
    rect = plt.Rectangle(
        (x0, y0),
        x1 - x0,
        y1 - y0,
        edgecolor= 'k',
        facecolor="none",
        linewidth=2, 
        zorder=6,
    )
    ax.add_patch(rect)
    
    ax.set(xlim = [-70, -40], ylim = [-20, -40])
    
    rect_width = lon1 - lon0
    rect_height = lat1 - lat0
    
    xc = (lon0 + lon1) / 2
    yc = (lat0 + lat1) / 2
    
    ell_width = rect_width * 0.45
    ell_height = rect_height * 1.3
    
    # ellipse1 = Ellipse(
    #     (xc, yc),
    #     width=ell_width,
    #     height=ell_height,
    #     angle=45,
    #     fill=False,
    #     edgecolor='k',
    #     lw=2
    # )
    
    ax.plot([lon0, lon1], [lat0, lat1])
    
    ellipse2 = Ellipse(
        (xc, yc),
        width=ell_width,
        height=ell_height,
        angle=-45,
        fill=False,
        edgecolor='k',
        lw=2
    )
    
    # ax.add_patch(ellipse1)
    ax.add_patch(ellipse2)
    
    ax.scatter(xc, yc)

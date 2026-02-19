import GOES as gs 
import matplotlib.pyplot as plt 
import cartopy.crs as ccrs
import base as b 
import datetime as dt 

 

def dn2fn(dn):
    
    fmt = "%Y%m%d%H%M.gz"
    date = dn.strftime('%Y/%m')
    infile = f'E:/database/goes/{date}/'
 
    return infile + 'S10236964_' + dn.strftime(fmt) 


fig, ax = plt.subplots(
    dpi = 300, 
    ncols = 3,
    figsize = (18, 10), 
    subplot_kw = 
    {'projection': ccrs.PlateCarree()}
    )

dn = dt.datetime(2016, 3, 5, 18, 0)

for i, ax in enumerate(ax.flat):
    
    delta = dt.timedelta(hours = 1)
    
    fname = dn2fn(dn + delta)
        
    ds = gs.CloudyTemperature(fname)
    
    dat, lon, lat = ds.data, ds.lon, ds.lat
    
    ptc = gs.plotTopCloud(dat, lon, lat, fig)
    img = ptc.contour(ax)

    ptc.add_map(ax)
    
    ax.set(title = ds.dn)
    
    if i == 2:
        ptc.colorbar(img, ax)
        
    if i > 0:
        ax.set(yticklabels = [], 
                ylabel = '')
        
    nl =  gs.find_nucleos(
              dat, 
              lon, 
              lat[::-1],
              ds.dn 
             
              )
    count = 0
    for index, row in nl.iterrows():
        count += 1
        ptc.plot_regions(
            ax,
            row['x0'], 
            row['y0'],
            row['x1'], 
            row['y1'], 
            number = count
            # i = indexs
            )
    

# dn2fn(dn)
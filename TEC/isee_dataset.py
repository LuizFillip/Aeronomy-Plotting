import xarray as xr
import cartopy.crs as ccrs
import datetime as dt
import matplotlib.pyplot as plt
import base as b 
import GEO as gg 
import pandas as pd 



def plot_map(ds):
    
    # ds = ds.where(
    #     ((ds['lon'] > -100) & 
    #     (ds['lon'] < -30) & 
    #     (ds['lat'] > -60) & 
    #     (ds['lat'] < 60)),
    #     drop = True  
    # )   

    fig, ax = plt.subplots(
          figsize = (10, 10), 
          dpi = 300, 
          subplot_kw = 
          {'projection': ccrs.PlateCarree()}
          )
    
    lat_lims = dict(min = -40, max = 40, stp = 10)
    lon_lims = dict(min = -100, max = -30, stp = 10) 
    
    
    
    gg.map_attrs(
        ax, 2015, 
        grid = False,
        degress = None, 
        lat_lims = lat_lims, 
        lon_lims = lon_lims,
        )
    
    
    img = ax.contourf(
        ds.lon.T,
        ds.lat, 
        ds.atec,
        30, 
        cmap = 'jet'
        )
    


def plot_latcutt(infile, ref_lon = -60):
    
    ds = xr.open_dataset(infile)
    
    ds = ds.isel(time = 0)
    
    ds = ds.where(ds.lon == ref_lon, drop = True)
    
    out = [ds.atec.values.flat, 
          ds.lat.values.flat]
    
    df = pd.DataFrame(out
        ).T 
    
    df.columns = ['tec', 'lat']
    
    return df.interpolate().set_index('lat')

out = []
for day in [13, 16, 18, 19]:
    infile = f'plotting/TEC/data/201512{day}22_atec.nc'
        
    out.append(plot_latcutt(infile))

df = pd.concat(out, axis = 1)
# plt.plot(df.tec, df.lat)



fig, ax = plt.subplots(
    dpi = 300, 
    figsize = (10, 10)
    )
df['avg'] = df.mean(axis = 1)

ax.plot(df.avg, df.index, label = 'Quiet-time', lw = 2)

infile = 'plotting/TEC/data/2015122022_atec.nc'

df = plot_latcutt(infile)

ax.plot(df.tec, df.index, label = 'Storm-time', lw = 2)

ax.set(
       ylabel = 'Latitude (°)',
       xlabel = 'TEC ($10^{16}/m^2$)'
       )
ax.legend()
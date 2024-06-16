import GEO as gg
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import xarray as xr 
import pandas as pd 
import base as b

infile = 'GAIA/data/netcdfs/'

b.config_labels()

parameter = 'efp'
file = f'{parameter}20130101cpl.nc'

ds = xr.open_dataset(infile + file)
ds['lon'] = ds['lon'] - 180

lat_lims = dict(min = -90, max = 90, stp = 30)
lon_lims = dict(min = -180, max = 180, stp = 60) 


def plot_contour(ds, times, parameter, height  = 300):
    
    sel_lvl = ds.sel(lvl = height)


    fig, ax = plt.subplots(
        figsize = (18, 12),
        dpi = 300, 
        ncols = 3, 
        nrows = 3, 
        subplot_kw = 
        {'projection': ccrs.PlateCarree()}
        )
    
    plt.subplots_adjust(wspace = 0.05, hspace = 0)
    vmin = sel_lvl[parameter].min()
    vmax = sel_lvl[parameter].max()
    
    step = (vmax - vmin) / 5
    
    ax[0, 0].text(
        0, 1.6, f'{height} km', 
        fontsize = 40,
        transform = ax[0, 0].transAxes
        )
    for i, ax in enumerate(ax.flat):
        time = times[i]
        dn = pd.to_datetime(time)
        
        gg.map_attrs(
            ax, dn.year, 
            grid = False,
            degress = None,
            lon_lims = lon_lims, 
            lat_lims = lat_lims
            )
        
        
        
        sel_ds = sel_lvl.sel(time = time)
        
        v = sel_ds[parameter].values
        x = sel_ds['lon'].values 
        y = sel_ds['lat'].values
        
        ax.pcolormesh(
            x, y, v, 
            vmin = vmin, 
            vmax = vmax, 
            cmap = 'rainbow'
            )
        

        ax.set(title = dn.strftime('%Hh%M (UT)'))
        
        if time != times[6]:
            
            ax.set(
                xticks = [],
                yticks = [], 
                ylabel = '', 
                xlabel = ''
                )
        
    attrs = ds[parameter].attrs
    name = attrs['long_name']
    units = attrs['units']

    
    b.fig_colorbar(
            fig,
            vmin, 
            vmax, 
            cmap = "rainbow",
            fontsize = 25,
            step = step,
            label = f'{name} ({units})', 
            sets = [0.3, 1.0, 0.5, 0.02], 
            orientation = 'horizontal'
            )
    
times = ds['time'].values[10::4]

plot_contour(ds, times, parameter, height = 100)





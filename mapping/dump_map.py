import cartopy.feature as cf
import numpy as np 
import cartopy.crs as ccrs
import matplotlib.pyplot as plt 
import epbs as pb 
import datetime as dt 

def plot_regions(
        ax,
        x_stt, y_stt, 
        x_end, y_end, 
        number = None
        ):
    
  
    rect = plt.Rectangle(
        (x_stt, y_stt), 
        x_end - x_stt, 
        y_end - y_stt,
        edgecolor = 'k', 
        facecolor = 'none', 
        linewidth = 3
    )
    
    ax.add_patch(rect)
    
    if number is not None:
        middle_y = (y_end + y_stt) / 2
        middle_x = (x_end + x_stt) / 2
        
        ax.text(
            middle_x, 
            middle_y + 1, number, 
            transform = ax.transData
            )
        
    return None 

def plot_map(df):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (10, 10), 
        subplot_kw = 
        {'projection': ccrs.PlateCarree()}
        )
    
    states = cf.NaturalEarthFeature(
        category = 'cultural',
        name = 'admin_1_states_provinces_lines',
        scale = '50m',
        facecolor = 'none'
        )
    
    args = dict(edgecolor = 'black', lw = 1)
    
    ax.add_feature(states, **args)
    ax.add_feature(cf.COASTLINE, **args) 
    ax.add_feature(
        cf.BORDERS, linestyle = '-', **args)
    
    ext = [-50, -30, -20, 10]
    ax.set_extent(
        ext, 
        crs = ccrs.PlateCarree()
        )
    
    ax.set_xticks(
        np.arange(ext[0], ext[1], 5), 
            crs = ccrs.PlateCarree()
        ) 
    
    ax.set_yticks(
        np.arange(ext[2], ext[3], 5), 
            crs = ccrs.PlateCarree()
        )
    
    
    ax.set(
        ylabel = 'Latitude (°)',  
        xlabel = 'Longitude (°)'
        ) 
    
    ax.scatter(df['lon'], df['lat'], c = df['roti'])
    
   
 
def load_and_filter(dn, root = 'D:\\'):
 
    df = pb.get_nighttime_roti(dn, root = root, hours = 10)
     
    stations = ['rnmo', 'pbcg', 
                'pepe', 'recf', 
                'rnna', 'pbjp']
    
    return df.loc[df['sts'].isin(stations)]

dn = dt.datetime(2011, 3, 2, 20)
df = load_and_filter(dn, root = 'D:\\')

df = df.loc[
    (df.lon > -40) & 
    (df.lon < -35) & 
    (df.lat > -10) & 
    (df.lat < -5)
    ]
 
plot_map(df)
import cartopy.feature as cf
import numpy as np 
import cartopy.crs as ccrs
import matplotlib.pyplot as plt 

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
    
    ax.set_extent(
        [-100, -30, 
        -70, 10], 
        crs = ccrs.PlateCarree()
        )
    
    ax.set_xticks(
        np.arange(-100, -30, 15), 
            crs = ccrs.PlateCarree()
        ) 
    
    ax.set_yticks(
        np.arange(-70, 10, 15
            ), 
            crs = ccrs.PlateCarree()
        )
    
    
    ax.set(
        ylabel = 'Latitude (°)',  
        xlabel = 'Longitude (°)'
        ) 
    
    for index, row in df.iterrows():
        
        plot_regions(
            ax,
            row['x0'], 
            row['y0'],
            row['x1'], 
            row['y1']
            )
        
        mx = (row['x1'] + row['x0']) / 2
        my = (row['y1'] + row['y0']) / 2
        ax.scatter(mx, my, s = 100, color = 'red')
        

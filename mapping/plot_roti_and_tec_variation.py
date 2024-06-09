import datetime as dt 
import plotting as pl
import base as b
import PlasmaBubbles as pb 
import GEO as gg 
import numpy as np 

b.config_labels(fontsize = 25)

    


def plot_sites_and_instrumention(ax):
    
    sites = ['ca',  'jic', 'saa'] 
    names = [
        'All-Sky (Cariri)', 
        'Ionosonde (Jicamarca)', 
        'Ionosonde (São Luis)'   
        ]  

    
    c = ['red', 'green', 'magenta']
    for i, site in enumerate(sites):
        
        glat, glon = gg.sites[site]['coords']
        
        ax.scatter(
            glon, glat, s = 150,
            c = c[i], marker = 's', 
            label = names[i])
    
    ax.legend(loc = 'lower right')
    
    
def range_time(start, mi):
        
    return start + dt.timedelta(minutes = mi)

def plot_mapping(ax_map, df, dn):

    gg.map_attrs(ax_map, dn.year, grid = False)

    gg.plot_rectangles_regions(ax_map, dn.year)
        
    lon, lat = gg.terminator2(dn, 18)
    
    ax_map.scatter(lon, lat, c = 'k', s = 5)
    
    sectors = np.arange(-80, -40, 10)[::-1]    
    
    delta = dt.timedelta(minutes = 5)
    
    for i, sector in enumerate(sectors):
        
        ds = pb.filter_region_and_dn(df, dn, sector)
        
        ds = ds.loc[ds.index > dn - delta]
        
        img = ax_map.scatter(
                  ds['lon'],
                  ds['lat'],
                  c = ds['roti'],
                  s = 30,
                  cmap = 'jet',
                  vmin = 0,
                  vmax = 4
              )       
    
    ticks = np.arange(0, 5, 1)
    b.colorbar(
            img, 
            ax_map, 
            ticks, 
            label = 'ROTI (TECU/min)', 
            height = '5%' , 
            width = "80%",
            orientation = "horizontal", 
            anchor = (-0.26, 0.7, 1.26, 0.5)
            )

def plot_roti_tec_variation(
        df, 
        start, 
        dn, 
        vmax = 100, 
        site = 'SAA0K', 
        fontsize = 30 
        ):
    
    fig, ax_map, axes = b.axes_and_map(
        figsize = (18, 12),
        nrows = 4, 
        wspace = 1.5
        )
    
    
    plot_mapping(ax_map, df, dn)
     
    pl.plot_roti_timeseries( 
        axes, 
         df, 
         dn, 
         start, 
         site,
         vmax = 3, 
         right_ticks = False,
         threshold = 0.25, 
         plot_drift = False 
         )
    
    plot_sites_and_instrumention(ax_map)
    
    fig.text(
        0.5, 0.45, 
        'ROTI (TECU/min)', 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.92, 0.45, 
        'OCCURRENCE', 
        fontsize = fontsize, 
        rotation = 'vertical',
        color = 'b'
        )
    
    for i in range(len(axes) - 1):
        b.adjust_axes_position(
            axes[i], axes[i + 1], 
                offset = 0.04 * (i + 1)
                )

        
    axes[-1].set(
        xlim = [df.index[0], df.index[-1]]
        )
    return fig

def main():
    
    start = dt.datetime(2014, 1, 2, 20)
    
    df =  pb.concat_files(
        start, 
        root = 'E:\\'
        )
    
    df = b.sel_times(df, start, hours = 12)
  
    dn = range_time(start, 400)
    
    fig = plot_roti_tec_variation(df, start, dn, vmax = 12)
    
    
    
main()
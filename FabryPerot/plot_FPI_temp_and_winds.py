import matplotlib.pyplot as plt
import FabryPerot as fp
import base as b
import datetime as dt

def get_dn(wd):
    return dt.datetime(
        wd.index[0].year, 
        wd.index[0].month, 
        wd.index[0].day, 
        21, 
        0)

 
b.config_labels()
    
def plot_directions( ax, path, site = 'car'):
    
    wd = fp.FPI(path).wind
    tp = fp.FPI(path).temp
            
    coords = {
        "Zonal": ("east", "west"), 
        "Meridional": ("north", "south")
        }
    
    for col, coord in enumerate(coords.keys()):
        
        ax[0, col].set(title = coord)
        
        for row, direction in enumerate(coords[coord]):
            # print(col, dirs)
            ds = wd.loc[(wd["dir"] == direction)]
            
            ax[0, col].errorbar(
                ds.index, 
                ds['vnu'], 
                yerr = ds["dvnu"], 
                label = direction, 
                capsize = 5
                    )
            
            ds = tp.loc[(tp["dir"] == direction)]
            
            
            ax[1, col].errorbar(
                ds.index, 
                ds['tn'], 
                yerr = ds['dtn'], 
                label = direction, 
                capsize = 5
                )
            
        b.format_time_axes(ax[1, col])
         
      
    ax[0, 0].set(ylabel = "Velocity(m/s)", ylim = [-100, 400])
    
    ax[1, 0].set(ylabel = "Temperature (K)", ylim = [700, 1200])
       
    for row, name in enumerate(coords.values()):
        ax[0, row].legend(name,
             ncol = 2, loc = 'upper center'
             )
        ax[1, row].legend(name,
             ncol = 2, loc = 'upper center'
             )
        
        ax[0, row].axhline(0, color = "k", linestyle = "--")
    


def plot_nighttime_observation(
        path, 
        ):
    
    fig, ax = plt.subplots(
        nrows = 2, 
        ncols = 2,
        figsize = (16, 8), 
        sharex =  'col',
        sharey = 'row',
        dpi = 300
        )
    
    plt.subplots_adjust(
        wspace = 0.1, 
        hspace = 0.1
        )
    
    if "car" in path:    
        site= "Cariri"
    elif 'bfp' in path:
       
        site = "Cachoeira Paulista"
    else:
        site = "Cajazeiras"
       
    plot_directions(ax, path, site = site)
        
    fig.suptitle(site)
    
    b.plot_letters(ax, y = 0.85, x = 0.03)
    return fig
        
def main():
    
    path = 'database/FabryPerot/cj/bfp220725g.7100.txt'
    
    path = 'database/FabryPerot/car/minime01_car_20150810.cedar.001.txt'
    fig = plot_nighttime_observation(path)
    

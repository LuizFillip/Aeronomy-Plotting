import matplotlib.pyplot as plt
import FabryPerot as fp
import base as b
import datetime as dt

b.config_labels()


def get_dn(wd):
    return dt.datetime(
        wd.index[0].year, 
        wd.index[0].month, 
        wd.index[0].day, 
        21, 
        0)

def sel_coord(ax, wd, direction, parameter = 'vnu'):
    ds = wd.loc[(wd["dir"] == direction)]
    
    ax.errorbar(
        ds.index, 
        ds[ parameter], 
        yerr = ds[f'd{parameter}'], 
        label = direction, 
        capsize = 5
            )
 
def title_site(path):
    if "car" in path:    
        site= "Cariri"
    elif 'bfp' in path:
        site = "Cachoeira Paulista"
    else:
        site = "Cajazeiras"

    fig.suptitle(site)
    
    
def plot_directions( ax, path):
    
    wd = fp.FPI(path).wind
    tp = fp.FPI(path).temp
    rl = fp.FPI(path).bright
    
    coords = {
        "Zonal": ("east", "west"), 
        "Meridional": ("north", "south")
        }
    
    for col, coord in enumerate(coords.keys()):
        
        ax[0, col].set(title = coord)
        
        for row, direction in enumerate(coords[coord]):
            
            sel_coord(ax[0, col], wd, direction, parameter = 'vnu')
            sel_coord(ax[1, col], tp, direction, parameter = 'tn')
            sel_coord(ax[2, col], rl, direction, parameter = 'rle')
    
        b.format_time_axes(ax[-1, col])
         
      
    ax[0, 0].set(ylabel = "Velocity (m/s)", ylim = [-100, 400])
    ax[1, 0].set(ylabel = "Temperature (K)", ylim = [800, 1400])
    ax[2, 0].set(ylabel = "Relative intensity (R)", ylim = [0, 200])
    
    ax[0, 0].legend(['east', 'west'],
         ncol = 2, 
         title = 'Zonal',
         loc = 'upper center'
         )
    
    ax[0, 1].legend(['north', 'south'],
         ncol = 2, 
         title = 'Meridional',
         loc = 'upper center'
         )
    
    for row, name in enumerate(coords.values()):
    
        
        ax[0, row].axhline(0, color = "k", linestyle = "--")
    
    return None

def plot_nighttime_observation(path):
    
    fig, ax = plt.subplots(
        nrows = 3, 
        ncols = 2,
        figsize = (16, 12), 
        sharex =  'col',
        sharey = 'row',
        dpi = 300
        )
    
    plt.subplots_adjust(
        wspace = 0.1, 
        hspace = 0.1
        )
    
    
        
    plot_directions(ax, path)
    
    b.plot_letters(ax, y = 0.85, x = 0.03)
    return fig
        

    
path = 'database/FabryPerot/cj/bfp220725g.7100.txt'


fig = plot_nighttime_observation(path)

FigureName = 'temp_winds_cajazeiras'


# fig.savefig(
#       b.LATEX(FigureName, folder = 'paper2'),
#       dpi = 400
#       )
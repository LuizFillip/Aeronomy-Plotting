import matplotlib.pyplot as plt
import FabryPerot as fp
import base as s
import models as m


def plot_directions(
        ax, 
        path, 
        parameter = "vnu"
        ):
    
    if parameter == "vnu":
        df = fp.FPI(path).wind
    else:
        df = fp.FPI(path).temp
                
    coords = {
        "zon": ("east", "west"), 
        "mer": ("north", "south")
        }
    
    names = ["zonal", "meridional"]
    
    infile = 'FabryPerot/data/winds_bjl'
    ds1 = s.load(infile)
    
    dn = df.index[-1].date()
    
    ds1 = ds1.loc[ds1.index.date == dn]
    
    for i, coord in enumerate(coords.keys()):
        
        ax[i].plot(ds1[coord], lw = 2, label = "HWM-14 (250 km)")
       
        for direction in coords[coord]:
            
            ds = df.loc[(df["dir"] == direction)]
            
            ax[i].errorbar(
                ds.index, 
                ds[parameter], 
                yerr = ds[f"d{parameter}"], 
                label = direction, 
                capsize = 5
                )
        ax[i].legend(loc = "lower left", ncol = 3)
        ax[i].set(ylabel = f"{names[i]} wind (m/s)", 
                  ylim = [-100, 200], 
                  xlim = [ds.index[0], ds.index[-1]])
        ax[i].axhline(0, color = "k", linestyle = "--")




def plot_nighttime_observation(
        path, 
        parameter = "vnu"
        ):
    
    fig, ax = plt.subplots(
        nrows = 2, 
        figsize = (10, 8), 
        sharex = True, 
        sharey = True, 
        dpi = 300
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    
    plot_directions(ax, path, parameter = parameter)
    
    s.format_time_axes(
            ax[1], 
            hour_locator = 1, 
            day_locator = 1, 
            tz = "UTC"
            )
    
    if "car" in path:    
        ax[0].set_title("Cariri")
    elif 'bfp' in path:
        ax[0].set_title("Cachoeira Paulista")
    else:
        ax[0].set_title("Cajazeiras")
   
    return fig
        
infile = 'FabryPerot/data/FPI/'
import os 

for file in os.listdir(infile):
    
    fig = plot_nighttime_observation(infile + file)
    
    fig.savefig('FabryPerot/img/' + file.replace('txt', 'png'))
import matplotlib.pyplot as plt
import FabryPerot as fp
import base as b
import numpy as np 

b.config_labels()
def plot_directions(ax, path, parameter = "vnu"):
    
    if parameter == "vnu":
        df = fp.FPI(path).wind
        vmax = round(df['vnu'].max())
        ylim = [-100, vmax]
        yticks = np.arange(ylim[0], ylim[-1], 50)
        units = '(m/s)'
    else:
        df = fp.FPI(path).temp
        ylim = [600, 1200]
        yticks = np.arange(ylim[0], ylim[-1], 100)
        units = '(K)'
                
    coords = {
        "zon": ("east", "west"), 
        "mer": ("north", "south")
        }
    
    names = ["zonal", "meridional"]
    
    for i, coord in enumerate(coords.keys()):
        
       
        for direction in coords[coord]:
            
            ds = df.loc[(df["dir"] == direction)]
            
            ax[i].errorbar(
                ds.index, 
                ds[parameter], 
                yerr = ds[f"d{parameter}"], 
                label = direction, 
                capsize = 5
                )
        ax[i].legend(loc = "upper right", ncol = 2)
        ax[i].set(
            ylabel = f"{names[i].title()} {units}", 
            ylim = ylim, 
            yticks = yticks,
            xlim = [ds.index[0], ds.index[-1]]
            )
        ax[i].axhline(0, color = "k", linestyle = "--")

    return None 


def plot_nighttime_observation(
        path, 
        parameter = "vnu"
        ):
    
    fig, ax = plt.subplots(
        nrows = 2, 
        figsize = (12, 8), 
        sharex = True, 
        sharey = True, 
        dpi = 300
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    plot_directions(ax, path, parameter = parameter)
    
    b.format_time_axes(ax[1])
    
    if "car" in path:    
        ax[0].set_title("Cariri")
    elif 'bfp' in path:
        ax[0].set_title("Cachoeira Paulista")
    else:
        ax[0].set_title("Cajazeiras")
        
    b.plot_letters(ax, y = 0.85, x = 0.03)
   
    return fig
        
# infile = 'FabryPerot/data/FPI/'
infile = 'database/FabryPerot/car/minime01_car_20140102.cedar.005.txt'
infile = 'database/FabryPerot/car/minime01_car_20151220.cedar.003.txt'


fig = plot_nighttime_observation(
    infile, parameter = 'vnu')

plt.show()
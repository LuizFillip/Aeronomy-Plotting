import matplotlib.pyplot as plt
import FabryPerot as fp
import settings as s
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
    

    for i, coord in enumerate(coords.keys()):
        
        ds = m.load_hwm(df, alt = 250, site = "car")
        
        ax[i].plot(ds[coord], lw = 2, label = "HWM-14 (250 km)")
        
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
                  ylim = [-100, 200])
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
    else:
        ax[0].set_title("Cajazeiras")
   
    return fig
        
def main():
    
 
    path = 'database/FabryPerot/car/minime01_car_20130216.cedar.005.txt'
    #path = 'database/FabryPerot/caj/minime02_caj_20121216.cedar.005.txt'
    fig = plot_nighttime_observation(path)
    
    # fig.savefig("FabryPerot/figures/20130318.png", dpi = 300)



main()
plt.show()
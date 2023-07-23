import datetime as dt
import os
import FabryPerot as fp
import settings as s
import matplotlib.pyplot as plt
import models as m
from utils import translate



    


def plot_directions2(
        ax, 
        path, 
        col = 0,
        parameter = "vnu"
        ):
    
    if "car" in path:    
        ax[0, col].set_title("Cariri")
    else:
        ax[0, col].set_title("Cajazeiras")
        
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
       
        ax[i, col].plot(ds[coord], lw = 2, label = "HWM-14 (250 km)")
       
        for direction in coords[coord]:
            
            ds = df.loc[(df["dir"] == direction)]
            if direction == "east":
                name = "Leste"
            elif direction == "west":
                name = "Oeste"
            elif direction == "north":
                name = "Norte"
            else:
                name = "Sul"
            ax[i, col].errorbar(
                ds.index, 
                ds[parameter], 
                yerr = ds[f"d{parameter}"], 
                label = name, 
                capsize = 5
                )
        ax[i, col].legend(loc = "lower left", ncol = 3)
        ax[i, col].set(
            ylabel = f"Vento {names[i]} (m/s)", 
            ylim = [-200, 200]
            )
        ax[i, col].axhline(0, color = "k", linestyle = "--")   
        ax[i, 1].set(ylabel = "")
        
    s.format_time_axes(
            ax[1, col], hour_locator = 1, 
            day_locator = 1, 
            tz = "UTC"
            )
    
    return ax



def get_datetime_fpi(filename):
    s = filename.split('_')
    obs_list = s[-1].split('.') 
    date_str = obs_list[0]
    return dt.datetime.strptime(
        date_str, "%Y%m%d")

def same_dates_in_sites(year = 2013):
    caj = "database/FabryPerot/caj/"
    car = "database/FabryPerot/2012/"
    
    out = []
    
    for f1 in os.listdir(caj):
        caj_dt = get_datetime_fpi(f1)
    
        for f2 in os.listdir(car):
    
            car_dt = get_datetime_fpi(f2)
            
            if ((car_dt == caj_dt) and 
                (car_dt.year == 2013) and 
                (car_dt.month == 3)):
                car_infile = os.path.join(car, f2)
                caj_infile = os.path.join(caj, f1)
                
                out.append(tuple((car_infile, caj_infile)))
    
    return out
            
        
         
def plot_both_sites(f1, f2):
    
    fig, ax = plt.subplots(
        nrows = 2, 
        ncols= 2,
        figsize = (18, 8), 
        sharex = True, 
        sharey = True, 
        dpi = 300
        )

    plt.subplots_adjust(hspace = 0.05, 
                        wspace = 0.05)

    for col, path in enumerate([f1, f2]):
        plot_directions2(
                ax, 
                path, 
                col = col,
                parameter = "vnu"
                )
    
    s.config_labels(fontsize = 18)
    return fig 




def save_img(fig, 
             save_in):
    
    plt.ioff()
    fig.savefig(save_in, 
                dpi = 300, 
                pad_inches = 0, 
                bbox_inches = "tight")
    plt.clf()   
    plt.close()
    return 

def main():

    for infiles in same_dates_in_sites(year = 2013):
        f1, f2 = infiles
        
    
        try:
            fig = plot_both_sites(f1, f2)
            FigureName = fp.date_from_filename(
                f1).strftime("%Y%m%d.png")
            save_in = "D:\\plots2\\FPI\\"
            print("saving...", FigureName)
            save_img(fig, os.path.join(save_in, FigureName))
        except:
            continue

# infiles = same_dates_in_sites(year = 2013)

# infiles





f1, f2 = ('database/FabryPerot/2012/minime01_car_20130317.cedar.005.txt',
 'database/FabryPerot/caj/minime02_caj_20130317.cedar.005.hdf5.txt')

# f1, f2 = ('database/FabryPerot/2012/minime01_car_20130316.cedar.005.txt',
#  'database/FabryPerot/caj/minime02_caj_20130316.cedar.005.hdf5.txt')

# f1, f2 = ('database/FabryPerot/2012/minime01_car_20130319.cedar.005.txt',
#  'database/FabryPerot/caj/minime02_caj_20130319.cedar.005.hdf5.txt')
fig = plot_both_sites(f1, f2)

FigureName = fp.date_from_filename(f1).strftime("%Y%m%d.png")

fig.savefig("FabryPerot/figures/" + FigureName, dpi = 300)
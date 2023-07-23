import matplotlib.pyplot as plt
import FabryPerot as fp
import os
import settings as s
import pandas as pd
import models as m
import datetime as dt

def get_dn(wd):
    return dt.datetime(
        wd.index[0].year, 
        wd.index[0].month, 
        wd.index[0].day, 
        21, 
        0)



def plot_directions(
        ax, 
        path, 
        site = 'car'):
    
    wd = fp.FPI(path).wind
    tp = fp.FPI(path).temp
        
    coords = {
        "zon": ("east", "west"), 
        "mer": ("north", "south")
        }
    

    for row, coord in enumerate(coords.keys()):
        

        # ds = m.load_hwm(wd, alt = 300, site = site)
        
        # ax[row, 0].plot(ds[coord], lw = 2, label = "HWM-14")
        
        # df = m.timerange_msis(get_dn(wd), site = site)

        # ax[row, 1].plot(df["Tn"], lw = 2, label = "MSIS-00")
        
        for direction in coords[coord]:
            
            ds = wd.loc[(wd["dir"] == direction)]
            
            ax[row, 0].errorbar(
                ds.index, 
                ds['vnu'], 
                yerr = ds["dvnu"], 
                label = direction, 
                capsize = 5
                )
            
            ds = tp.loc[(tp["dir"] == direction)]
            
            ax[row, 1].errorbar(
                ds.index, 
                ds['tn'], 
                yerr = ds['dtn'], 
                label = direction, 
                capsize = 5
                )
            
        ax[row, 0].legend(loc = "upper right", ncol = 1)
        ax[row, 1].legend(loc = "upper right", ncol = 1)
        
        
        ax[row, 0].set(
            ylabel = "Velocidade (m/s)", 
            ylim = [-100, 150])
        
        ax[row, 1].set(ylabel = "Temperatura (K)", 
                  ylim = [600, 1200])

        ax[row, 0].axhline(0, color = "k", linestyle = "--")

        s.format_time_axes(
                ax[1, row], hour_locator = 1, 
                day_locator = 1, 
                tz = "UTC"
                )
    
    names = ["zonal", "zonal", "meridional", "meridional"]

    for i, ax in enumerate(ax.flat):
        letter = s.chars()[i]
        ax.text(
            0.02, 0.85, f"({letter}) {names[i].title()}", 
            transform = ax.transAxes
            )
    return None


def plot_nighttime_observation(
        path, 
        ):
    
    fig, ax = plt.subplots(
        nrows = 2, 
        ncols= 2,
        figsize = (16, 10), 
        sharex = True, 
        dpi = 300
        )
    
    plt.subplots_adjust(
        wspace = 0.2, 
        hspace = 0.1
        )
    
    if "car" in path:    
        title = "Cariri"
        site = 'car'
    else:
        title = "Cajazeiras"
        site = 'car'
    plot_directions(ax, path, site = site)
        
    fig.suptitle(title)
    return fig
        
def main():
    
    
    path = 'database/FabryPerot/2012/minime01_car_20130318.cedar.005.txt'
    
    path = "database/FabryPerot/car/minime01_car_20130909.cedar.006.txt"
   
    fig = plot_nighttime_observation(path)
    
    
def save_plots():
    
    infile = "database/FabryPerot/2012/"

    files = os.listdir(infile)
    save = 'D:\\plots\\car\\'


    def fn2dn(filename):
        dn = filename.split('.')[0].split('_')[-1]
        return dt.datetime.strptime(dn, '%Y%m%d')  

    for filename in files:
        dn = fn2dn(filename)
        
        # if (dn.year == 2013) and (dn.month == 3):
            # print(filename)
            
        FigureName = dn.strftime('%Y%m%d.png')
        
        plt.ioff()
        print(dn)
        fig = plot_nighttime_observation(infile + filename)
        
        fig.savefig(save + FigureName, dpi = 300)
        
        plt.clf()   
        plt.close()
        
# main()
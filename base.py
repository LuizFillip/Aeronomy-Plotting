import os
import datetime as dt
from liken.plotting.plot_nighttime_corr_FPI_EPB import plot_nigthttime_corr_FPI_EPB
import matplotlib.pyplot as plt
import pandas as pd


def get_datetime_fpi(filename):
    s = filename.split('_')
    obs_list = s[-1].split('.') 
    date_str = obs_list[0]
    return dt.datetime.strptime(
        date_str, "%Y%m%d")

def get_datetime_epb(filename):
    year, mon_day, lat = tuple(filename.replace(".txt", "").split("_"))
    month = int(mon_day[:2])
    day = int(mon_day[2:])
    year = int(year)
    
    if lat == "":
        lat = 0
    else:
        lat = int(lat)
    return dt.datetime(year, month, day), lat



def save_img(fig, 
             save_in):
    
    plt.ioff()
    fig.savefig(save_in, 
                dpi = 100, 
                pad_inches = 0, 
                bbox_inches = "tight")
    plt.clf()   
    plt.close()
    return 



infile_epb = "database/EPBs/drift/"
infile_fpi = "database/FabryPerot/2012/"



def find_sames(lat_check = 5, 
               threshold = 0.6):
    out = []
    for f1 in os.listdir(infile_epb):
        date_epb, lat = get_datetime_epb(f1)
    
        for f2 in os.listdir(infile_fpi):
    
            date_fpi = get_datetime_fpi(f2)
                    
            if (date_fpi == date_epb) and (lat == lat_check):
                FPI_file = os.path.join(infile_fpi, f2)
                EPB_file = os.path.join(infile_epb, f1)
                try:
                    FigureName =  f1.replace("txt", "png")
                    save_in = os.path.join(
                        "C:\\plots",
                        FigureName
                        )
                    fig, r2, df = plot_nigthttime_corr_FPI_EPB(
                        FPI_file, 
                        EPB_file,
                        lat
                        )
                    
                    save_img(fig, save_in)
                    
                    if r2 > threshold:
                        out.append(df)
    
                except:
                    continue      
                
    
    ts = pd.concat(out)
    
    ts.to_csv("corr_06.txt", index = True)
    return ts


ts = find_sames(lat_check = 5)
print(ts)
       
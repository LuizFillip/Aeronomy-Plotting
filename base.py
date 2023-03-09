import os
import datetime as dt
from liken.plotting.plot_nighttime_corr_FPI_EPB import plot_nigthttime_corr_FPI_EPB
import matplotlib.pyplot as plt
import pandas as pd
from liken.utils import get_datetime_epb, get_datetime_fpi, save_img



infile_epb = "database/EPBs/drift/"
infile_fpi = "database/FabryPerot/2012/"



def find_sames(lat_check = 5, 
               threshold = 0.7):
    out = []
    for f1 in os.listdir(infile_epb):
        date_epb, lat = get_datetime_epb(f1)
    
        for f2 in os.listdir(infile_fpi):
    
            date_fpi = get_datetime_fpi(f2)
                    
            if (date_fpi == date_epb) and (lat == lat_check):
                FPI_file = os.path.join(infile_fpi, f2)
                EPB_file = os.path.join(infile_epb, f1)
                try:
                    FigureName = f1.replace("txt", "png")
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
       
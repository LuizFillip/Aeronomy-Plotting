import os
import datetime as dt
from liken.plotting.plot_nighttime_corr_FPI_EPB import plot_nigthttime_corr_FPI_EPB

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

infile_epb = "database/EPBs/"
infile_fpi = "database/FabryPerot/2013/"

for f1 in os.listdir(infile_epb ):
    date_epb, lat = get_datetime_epb(f1)

    for f2 in os.listdir(infile_fpi):

        date_fpi = get_datetime_fpi(f2)
                
        if (date_fpi == date_epb) and (lat == 5):
            FPI_file = os.path.join(infile_fpi, f2)
            EPB_file = os.path.join(infile_epb, f1)
            try:
                fig = plot_nigthttime_corr_FPI_EPB(
                    FPI_file, EPB_file
                    )
            except:
                continue      


       
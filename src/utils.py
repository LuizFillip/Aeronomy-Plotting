
import datetime as dt

def rename_cols(obs, name= "FPI"):

    obs = obs.rename(
         columns = {"zon": "zon_" + name, 
                    "mer": "mer_" + name}
         )
    
    return obs

def get_datetime_fpi(filename):
    s = filename.split('_')
    obs_list = s[-1].split('.') 
    date_str = obs_list[0]
    return dt.datetime.strptime(
        date_str, "%Y%m%d")

def get_datetime_epb(filename):
    year, mon_day, lat = tuple(
        filename.replace(".txt", "").split("_"))
    month = int(mon_day[:2])
    day = int(mon_day[2:])
    year = int(year)
    
    if lat == "":
        lat = 0
    else:
        lat = int(lat)
    return dt.datetime(year, month, day), lat










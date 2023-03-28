import datetetime as dt
import pandas as pd

class date_from_filename(object):
    
    """Convert digisonde, imager and TEC files filename (EMBRACE format) to datetime"""
    
    def __init__(self, file):
        
        extension = file[-4:]
        
        
        if ((extension == ".SAO") or 
            (extension == ".RSF")):
            
            args = file[:-4].split("_")
            year = int(args[1][:4])
            doy = int(args[1][4:7])
            hour = int(args[1][7:9])
            minute = int(args[1][9:11])
            
            date = dt.date(year, 1, 1) + dt.timedelta(doy - 1)
        
            day = date.day
            month = date.month
        
            self.datetime = dt.datetime(year, month, day,
                                              hour, minute)
            
            
        elif "(" in file:
            
           
            arg = file.split("_")[1][:-4]
            
            self.datetime = dt.datetime.strptime(arg, "%Y%m%d(%j)%H%M%S")
            
        elif ((extension == ".PNG") or
              (extension == ".tif")):
            
            args = file[:-4].split("_")
            
            date = args[2]
            time = args[3]
            self.datetime = dt.datetime.strptime(date + time, 
                                                 "%Y%m%d%H%M%S")
            
        elif ((extension == ".txt") or 
             ("TECMAP" in file)):
            
            args = file[:-4].split("_")
            
            date = args[1]
            time = args[2] 
            self.datetime = dt.datetime.strptime(date + time, "%Y%m%d%H%M")

def tec_format(time):
     return f"TECMAP_{time.strftime('%Y%m%d_%H%M')}.txt"
def iono_format(time):
    return f"FZA0M_{time.strftime('%Y%m%d(%j)%H%M%S')}.PNG"
      
def ordering(date, image_files):
    
    delta = dt.timedelta(days = 1)
    
    times = pd.date_range(f"{date} 21:00", 
                              f"{date + delta} 07:00", 
                              freq = "10min")
    out = []
    for z in range(len(times)):
        if times[z] < date_from_filename(image_files[0]).datetime:
            out.append([tec_format(times[z]), iono_format(times[z]), None])


    for y in range(len(times) - 1):                                                       
        for x in range(len(image_files)):
            imagerFilename = image_files[x]
            ref_time = date_from_filename(imagerFilename).datetime

            if (ref_time >= times[y]) and (ref_time <= times[y + 1]):
                out.append([tec_format(times[y]), iono_format(times[y]), imagerFilename])

    for w in range(len(times)):
        if times[w] > date_from_filename(image_files[-1]).datetime:
            out.append([tec_format(times[w]), iono_format(times[w]), None])
            
    return out
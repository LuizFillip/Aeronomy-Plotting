import pandas as pd
from main import FabryPerot, get_mean 
import setup as s
import matplotlib.pyplot as plt
import matplotlib.dates as dates


s.config_labels()




def plotCoord(ax, df, fp, zonal = False):
    
    if zonal:
        coord = "zon"
    else:
        coord = "mer"

    for site in ["car", "for"]:
    
        df_ = df.loc[df["site"] == site]
        
        ax.plot(df_[coord], label = f"HMW14 ({site})", lw = 2)
        
    mn = get_mean(fp, zonal = zonal, sample = "10min")
    
    ax.plot(mn, label = "FPI (car)", color = "k", lw = 2)

    ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
    ax.xaxis.set_major_locator(dates.HourLocator(interval = 1))
   
    return fig, ax
infile = "database/HWM/20140101.txt"

df = pd.read_csv(infile, index_col = "time")

df.index = pd.to_datetime(df.index)



infile = "database/minime01_car_20140101.cedar.007.txt"

fp = FabryPerot(infile).wind


fig, ax = plt.subplots(figsize = (10, 6), 
                       sharex = True, 
                       nrows = 2)


plt.subplots_adjust(hspace = 0.1)
plotCoord(ax[0], df, fp, zonal = True)
plotCoord(ax[1], df, fp, zonal = False)

ax[0].legend()

ax[0].set(ylabel = "Vento zonal (m/s)", title = "")
ax[1].set(xlabel = "Hora universal", 
       ylabel = "Vento meridional (m/s)")


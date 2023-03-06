import pandas as pd
import matplotlib.pyplot as plt
from FabryPerot.core import FabryPerot
from Results.read_diego_files import get_mean_vals
import datetime as dt
import setup as s
from FabryPerot.base import running_avg


f1 = 'database/FabryPerot/2013/minime01_car_20130109.cedar.005.txt'
f2 = 'G:\\My Drive\\Python\\data-analysis\\database\\KTC_RES\\KTC_2013_0109\\KTC_2013_0109_-5\\KTC_2013_0109_-5-00\\Keo_Tec_Geo_2013_0109.txt'


date = dt.datetime(2013, 1, 9)

epbs = get_mean_vals(f2, date)
wind = FabryPerot(f1).wind
avg = running_avg(wind, Dir = "zon")

fig, ax = plt.subplots(figsize = (10, 4), 
                       ncols = 2)


def plot_time_series(ax, wind, avg, epbs):
    
    ax.errorbar(epbs.index,
                epbs["vel"], 
                epbs["err"],
                capsize = 4,
                color = "r", 
                lw = 1.5,
                label = "EPBs")
    
    ax.plot(avg, color = "k", label = "Média")
    
    for up in ("east", "west"):
        
        zon = wind.loc[(wind["dir"] == up)]
        
        ax.errorbar(zon.index, 
                    zon["vnu"], 
                    yerr = zon["dvnu"], 
                    label = up)
    
    ax.legend()                  
    
    title = wind.index[0].strftime("%d/%m/%Y")
    
    ax.set(title = title,
           xlabel = "Hora universal", 
           ylabel = "Velocidade zonal (m/s)")
    s.format_axes_date(ax, time_scale= "hour")
    
    
plot_time_series(ax[0], wind, avg, epbs)

df = pd.concat([epbs, avg], axis = 1).dropna()

ax[1].scatter(df["zon"], df["vel"])
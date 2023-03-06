import pandas as pd
import matplotlib.pyplot as plt
from FabryPerot.core import FabryPerot
from Results.read_diego_files import get_mean_vals
import datetime as dt
import setup as s
from FabryPerot.base import running_avg
from Liken.utils import get_fit


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
    
    ax.axhline(0, color = "r", linestyle = "--")
    ax.legend()                  
    
    title = wind.index[0].strftime("%d/%m/%Y")
    
    ax.set(title = title,
           xlabel = "Hora universal", 
           ylabel = "Velocidade zonal (m/s)")
    s.format_axes_date(ax, time_scale= "hour")
    
        


def plot_scatter_corr(ax, df):
   
    x, y = df["zon"].values, df["vel"].values
    
    ax.scatter(x, y,  color = "k")

    x = x.reshape(-1, 1)
    y = y.reshape(-1, 1)
    
    r2, fit = get_fit(x, y)
     
    ax.plot(x, fit, 
            color = "k", 
            lw = 2,
            label = f"$R^2 = {r2}$")
    
    ax.legend()
    
    ax.set(ylabel = "EPBs", 
           xlabel = "FPI", 
           title = "Correlação")
    
    return df


def main():
    f1 = 'database/FabryPerot/2013/minime01_car_20130112.cedar.005.txt'
    f2 = 'database/KTC_RES/KTC_2013_0112/KTC_2013_0112_-5/KTC_2013_0112_-5-00/Keo_Tec_Geo_2013_0112.txt'
        
    epbs = get_mean_vals(f2)
    wind = FabryPerot(f1).wind
    avg = running_avg(wind, Dir = "zon")
    
    
    df = epbs.join(avg).dropna()
     
    fig, ax = plt.subplots(figsize = (10, 4), 
                           ncols = 2)
    
    plot_time_series(ax[0], wind, avg, epbs)
    
    plot_scatter_corr(ax[1], df)
    ax[0].axvspan(df.index[0], 
                  df.index[-1],
                  alpha = 0.3, 
                  color = "gray")
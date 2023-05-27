import matplotlib.pyplot as plt
from FabryPerot.core import FabryPerot
import settings as s
from FabryPerot import running_avg
from liken.utils import get_fit
from liken.core import load_EPB
import pandas as pd

def plot_HWM(ax, dat):
    f3 = "database/HWM/car_250_2013.txt"
    
    df = pd.read_csv(f3, index_col = "time")
    df.index = pd.to_datetime(df.index)

    df = df.loc[(df.index >= dat.index[0]) & 
                 (df.index <= dat.index[-1]), ["zon"]]
    
    ax.plot(df, lw = 2, label = "HWM-14")
    
    ax.legend(loc = "upper right")
    
    
def plot_time_series(ax, wind, avg, epbs):
    
    ax.errorbar(epbs.index,
                epbs["vel"], 
                epbs["err"],
                capsize = 4,
                color = "r", 
                lw = 1.5,
                label = "EPBs")
    
    ax.plot(avg, 
            lw = 2, 
            color = "k", 
            label = "Média")
    
    for up in ("east", "west"):
        
        zon = wind.loc[(wind["dir"] == up)]
        
        ax.errorbar(zon.index, 
                    zon["vnu"], 
                    yerr = zon["dvnu"], 
                    label = up, 
                    capsize = 3)
    
    ax.axhline(0, color = "r", linestyle = "--")
    ax.legend(loc = "upper right")                  
    
    title = wind.index[0].strftime("%d/%m/%Y")
    
    ax.set(title = title,
           ylim = [-50, 250],
           xlabel = "Hora universal", 
           ylabel = "Velocidade zonal (m/s)")
    s.format_axes_date(ax, time_scale= "hour", 
                       interval = 1)
    
        

def plot_scatter_corr2(ax, x, y):
    
    ax.scatter(x, y, color = "k")

    x = x.reshape(-1, 1)
    y = y.reshape(-1, 1)
    
    r2, fit = get_fit(x, y)
     
    ax.plot(x, fit, 
            color = "k", 
            lw = 2)
        
    ax.set(ylabel = "EPBs", 
           xlabel = "FPI", 
           title =  f"$R^2 = {r2}$", 
           ylim = [40, 200], 
           xlim = [40, 200])
    
    return r2


def plot_scatter_corr(ax, x, y):
   
    ax.scatter(x, y, color = "k")

    x = x.reshape(-1, 1)
    y = y.reshape(-1, 1)
    
    r2, fit = get_fit(x, y)
     
    ax.plot(x, fit, 
            color = "k", 
            lw = 2)
        
    ax.set(ylabel = "EPBs", 
           xlabel = "FPI", 
           title =  f"$R^2 = {r2}$", 
           ylim = [40, 200], 
           xlim = [40, 200])
    
    return r2


def plot_nigthttime_corr_FPI_EPB(
        fpi_file, 
        epbs_file, lat = 5
        ):
   
    epbs = load_EPB(epbs_file, lat = None)
    wind = FabryPerot(fpi_file).wind
    avg = running_avg(wind, Dir = "zon")

    df = epbs.join(avg).dropna()
    
    fig, ax = plt.subplots(figsize = (12, 5), 
                           ncols = 2)
    
    plot_time_series(ax[0], wind, avg, epbs)
    plot_HWM(ax[0], avg)
    x1, y1 = df["zon"].values, df["vel"].values
    r2 = plot_scatter_corr(ax[1], x1, y1)
    
    ax[0].axvspan(df.index[0], 
                   df.index[-1],
                   alpha = 0.3, 
                   color = "gray")

    fig.suptitle(f"Latitude: - {lat}°")
    return fig, r2, df

def main():
    f1 = 'database/FabryPerot/2013/minime01_car_20131115.cedar.007.txt'
    f2 = 'database/EPBs/2013_1115_20.txt'
    plot_nigthttime_corr_FPI_EPB(f1, f2)
    
#main()


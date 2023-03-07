import matplotlib.pyplot as plt
from FabryPerot.core import FabryPerot
import setup as s
from FabryPerot.base import running_avg
from liken.utils import get_fit
from liken.core import load_EPB

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
    
        


def plot_scatter_corr(ax, df):
   
    x, y = df["zon"].values, df["vel"].values
    
    ax.scatter(x, y,  color = "k")

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
    
    return df


def plot_nigthttime_corr_FPI_EPB(
        fabry_perot_file, 
        epbs_file, lat = 5
        ):
   
    epbs = load_EPB(epbs_file, lat = None)
        
    wind = FabryPerot(fabry_perot_file).wind
    
    avg = running_avg(wind, Dir = "zon")
    s    
    df = epbs.join(avg).dropna()
     
    fig, ax = plt.subplots(figsize = (12, 5), 
                           ncols = 2)
    
    plot_time_series(ax[0], wind, avg, epbs)
    
    plot_scatter_corr(ax[1], df)
    ax[0].axvspan(df.index[0], 
                   df.index[-1],
                   alpha = 0.3, 
                   color = "gray")
    fig.suptitle(f"Latitude: - {lat}°")
    return fig

def main():
    f1 = 'database/FabryPerot/2013/minime01_car_20131115.cedar.007.txt'
    f2 = 'database/EPBs/2013_1115_20.txt'
    plot_nigthttime_corr_FPI_EPB(f1, f2)
    
#main()
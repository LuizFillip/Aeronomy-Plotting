import numpy as np
import matplotlib.pyplot as plt
from omni import postdamData, OMNI2Data
import settings as s
from datetime import datetime, timedelta
from utils import compute_ticks

def plot_solar_flux(ax, 
                  years = [2008, 2022], 
                  yshade = 2014):
    
    """Plotting Solar flux F10.7 cm"""
    
    sflux = postdamData(infile = "database/postdam.txt")
    
    sflux = sflux.loc[(sflux.index.year >= years[0]) & 
                      (sflux.index.year <=   years[-1]) & 
                      (sflux["F10.7obs"] > 10) & 
                      (sflux["F10.7obs"] < 500)]
    
    
    ax.plot(sflux["F10.7obs"], lw = 0.8, color = "k")
    
    ax.set(ylabel = "$_{F10,7} $ cm", 
           yticks = np.arange(100, 450, 100), 
           xlabel = "Anos", 
           xlim = [datetime(years[0], 1, 1), 
                   datetime(years[-1], 12, 31)])
    
    if yshade:
        date = datetime(yshade, 1, 1)
        end = date + timedelta(days = 366)
        ax.axvspan(date, 
                   end,
                   alpha = 0.5, color = "gray")
        
        ax.text(end + timedelta(days = 5), 300, yshade, 
                transform = ax.transData)

    
    
def plot_disturbance_indexes(
        ax, 
        df, 
        col = "dst"
        ):
    
    """Plotting Disturbance Storm and Kp indexes"""
    
    args = dict(linestyle = "--", color = "k", lw = 1)
    
    if col == "dst":
        ax.plot(df[col], lw = 1, color = "k")
        ax.axhline(0, **args)
        
        vmin, vmax, step = compute_ticks(df[col])
        
        ax.set(ylabel = "Dst (nT)", 
               ylim = [vmin - step, vmax], 
               yticks = np.arange(vmin, 
                                  vmax + step, step)
               )
    else:
        y = df[col]
        x = df.index
        ax.axhline(4, **args)
        ax.bar(x, y, width = 2, color = "k")
    
        ax.set(ylabel = "Índice Kp", 
               ylim = [0, 9],
               yticks = np.arange(0, 10, 2)
                       )
    
    s.format_axes_date(ax)
    
    return ax
    
def plot_auroral_indexes(ax, df):
    
    """Plotting auroral indexes"""
    
    args = dict(lw = 1)
    
    ax.plot(df['ae'], color = "k", **args)
    
    ax1 = ax.twinx()
    
    p1, = ax1.plot(df["al"], **args)
    
    s.change_axes_color(ax1, p1)
    
    ax.axhline(0, linestyle = "--", 
               color = "k", **args)
    
    vmin, vmax, step = compute_ticks(df['ae'])
                        
    ax1.set(ylabel = "AL (nT)", 
            ylim = [-vmax, vmax], 
            yticks = np.arange(-vmax, 
                                vmax + step, step))
    
    ax.set(ylabel = "AE (nT)", 
            ylim =  [-vmax, vmax], 
            yticks = np.arange(-vmax, 
                                vmax + step, step))
    
    
    s.format_axes_date(ax)
        
def plotIndices(year = 2013):
    
    
    fig = plt.figure(figsize = (10, 8))
    
    s.config_labels()
    
    gs = fig.add_gridspec(1, bottom = 0.98, top = 1.2)
    
    ax1 =  gs.subplots()
        
    plot_solar_flux(ax1, yshade = year)

    gs = fig.add_gridspec(3, hspace = 0.1)
    
    (ax2, ax3, ax4) = gs.subplots(sharex = 'col')
    
    df = OMNI2Data(infile = "database/omni.txt",
                   year = year, parameter = None)
    
    plot_disturbance_indexes(ax2, df)
    
    plot_disturbance_indexes(ax3, df, 
                         col = "kp")
     
    plot_auroral_indexes(ax4, df)
    
    ax4.set(xlabel = "Meses")
    
    s.text_painels([ax1, ax2, ax3, ax4], 
                   x = 0.01, y = 0.85)

    plt.show()
    
    return fig
    
def main():
    plotIndices(year = 2015)
        
    #fig.savefig("img/PlanetaryIndices.png")
    
# main()
year = 2013
df = OMNI2Data(infile = "database/PlanetaryIndices/omni.txt",
               year = year, parameter = None)
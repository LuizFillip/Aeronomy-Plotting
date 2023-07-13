import settings as s
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from labels import y_label
from common import load_by_alt_time
import digisonde as dg
from utils import smooth2



def plot_ne_L(ax, df):
    
    ax.plot(df["L"] * 1e5)
    ax.set(ylabel = '$L^{-1}~(10^{-5}~m^{-1})$',
           ylim = [-7, 7])
    
    ax.axhline(0, linestyle = "--")
    
    # ax1 = ax.twinx()
    
    # p, = ax1.plot(df["ne"], color = '#0C5DA5')
  
    
    # ax1.set(ylabel = y_label('ne'))
    # s.change_axes_color(ax1, p)
    

def plot_nui_g(ax, df):
    
    ax.plot(9.81 / df["nui"], color = "k")
  
    ax.set(ylabel = y_label('gravity'), 
           ylim = [10, 50])
    
    
def plot_vertival_drift(ax, df):
    
    infile = "database/Digisonde/SAA0K_20130216_freq.txt"

    vz = dg.drift(pd.read_csv(
        infile, index_col = 0
        ),
        sel_columns = [6, 7, 8]
        )
    
    vz.index = pd.to_datetime(vz.index)
    
    vz = vz.loc[(vz.index >= df.index[0]) &
                (vz.index <= df.index[-1])]


    vz['avg'] = smooth2(vz['avg'], 7)

    vz = vz.interpolate()
    ax.plot(vz["avg"], color = "k")
    ax.axhline(0, linestyle = "--")
   
    ax.set(ylabel = y_label('vz'), 
           ylim = [-70, 70])
    
def plot_winds(ax, df):
    
    ax.plot(df["mer_ef"], label = "Paralelo a B")
    ax.plot(df["mer_perp"], label = "Perpendicular a B")
    ax.axhline(0, linestyle = "--")

    ax.set(ylabel = "$u_n$ (m/s)",  ylim = [-40, 40])
    ax.legend(loc = "lower left", ncol = 2)



def plot_rt_parameters_timeseries(df):
    
    
    
    fig, ax = plt.subplots(
        nrows = 4, 
        dpi = 300,
        sharex = True, 
        figsize = (10, 10)
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    plot_nui_g(ax[0], df)
    
    plot_ne_L(ax[1], df)
    
    plot_vertival_drift(ax[2], df)
    
    plot_winds(ax[3], df)
    
    s.config_labels()
    s.format_time_axes(
            ax[3], hour_locator = 1, 
            day_locator = 1, 
            tz = "UTC"
            )
    
    names = ['Gravidade',
             'Gradiente de escala do plasma', 
             'Deriva vertical',
             "Ventos meridionais (FPI)"]
    
    for i, ax in enumerate(ax.flat):
        letter = s.chars()[i]
        ax.text(
            0.02, 0.85, f"({letter}) {names[i]}", 
            transform = ax.transAxes
            )

    
    return fig

def main():

    alt = 300
    for i in [16, 17, 18]:
        dn = dt.datetime(2013, 3, i, 20)
        infile = "gamma_perp_mer.txt"
        
        df = load_by_alt_time(infile, alt, dn)
        
        
        fig = plot_rt_parameters_timeseries(df)
        

# main()
import settings as s
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from labels import Labels, y_label
from utils import save_img

def plot_ne_L(ax, df):
    
    ax.plot(df["L"])
    ax.set(ylabel = y_label('L'),
           ylim = [0.5e-5, 4e-5])
    
    ax1 = ax.twinx()
    
    p, = ax1.plot(df["Ne"], color = '#0C5DA5')
    title1 = Labels().infos["ne"]["name"]
    title2 = Labels().infos["L"]["name"]
    
    ax1.set(ylabel = y_label('ne'), 
            ylim = [1e5, 8e5], 
            title = f"{title2} e {title1}")
    s.change_axes_color(ax1, p)
    

def plot_nui_g(ax, df):
    
    ax.plot(9.81 / df["nui"], color = "k")
    title2 = Labels().infos["gravity"]["name"]
  
    ax.set(ylabel = y_label('gravity'), title = title2,
           ylim = [5, 15])
    
    
def plot_vertival_drift(ax, df):
    
    ax.plot(df["vz"], color = "k")
    ax.axhline(0, linestyle = "--")
    title2 = Labels().infos["vz"]["name"]
   
    ax.set(ylabel = y_label('vz'), 
           title = title2,
           ylim = [-70, 70])
    
def plot_winds(ax, df):
    
    ax.plot(df["U"], label = "zonal")
    ax.plot(df["V"], label = "meridional")
    ax.axhline(0, linestyle = "--")

    ax.set(ylabel = "Velocidade (m/s)", 
           title = "Ventos neutros (FPI)", 
           ylim = [-50, 200])
    ax.legend()


def sel_night(alt, dn):
    df = pd.read_csv("gamma_parameters.txt", index_col = 0)
    df.index = pd.to_datetime(df.index)
    
    return df.loc[(df["alt"] == alt) & (df.index >= dn) &
                (df.index <= dn + dt.timedelta(seconds = 43200))]


dn = dt.datetime(2013, 9, 20, 20)
alt = 250

def plot_rt_parameters_timeseries(dn, alt):
    
    df = sel_night(alt, dn)
    
    fig, ax = plt.subplots(
        nrows = 4, 
        dpi = 300,
        sharex = True, 
        figsize = (10, 10)
        )
    
    
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
    
    fig.suptitle(f"Variação dos parâmetros locais da $\\gamma_{{RT}}$ em {alt} km")
    
    return fig

def main():
   
    times =  pd.date_range(
        dt.datetime(2013, 9, 17, 20), 
        dt.datetime(2013, 9, 28, 20), 
        freq = "1D"
        )
    
    
    save_in = "D:\\plots2\\local_parameters\\"
    
    for dn in times:
        print("saving...", dn)
        fig = plot_rt_parameters_timeseries(dn, alt)
        FigureName = dn.strftime("%Y%m%d.png")
        save_img(fig, save_in + FigureName)
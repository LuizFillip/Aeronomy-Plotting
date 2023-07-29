import base as s
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import digisonde as dg



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
  
    
def plot_vertival_drift(ax, df):
    
    ...
   
   
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

path = 'FluxTube/data/reduced/SAA/'

def dataset(path):
    
    out = [
           ]
    
    for year in range(2013, 2016):
        
        ds = s.load(path + f'300_{year}.txt') 
        
        if year == 2013:
            ds['ratio'] = ds['ratio'] / 2
            
        out.append(ds)
   
    return pd.concat(out).dropna()

    
def main():
    for year in range(2013, 2016):
        ds = pd.read_csv(f'{year}02012000.txt', 
                         index_col = 0)
        
        plt.plot(ds['Te'], ds.alt)


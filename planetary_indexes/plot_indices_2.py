import matplotlib.pyplot as plt
import settings as s
from common import plot_terminators, load
import datetime as dt
import FabryPerot as fp
import digisonde as dg
from utils import smooth2, split_time
import pandas as pd

def plot_mag_electron(ax, infile):
    
    df = load(infile + 'omni_2012_2015.lst')
    
    df = df.loc[~((df['BZ'] > 990) | 
                  (df['Ey'] > 990))]

    ax.plot(df['BZ'])
    
    ax.set(ylim = [-25, 25], 
           ylabel = "$B_z$ (nT)")
    
    ax1 = ax.twinx()
    
    line, = ax1.plot(df['Ey'], color = '#0C5DA5')
    
    ax1.set(ylim = [-25, 25], ylabel = "$E_y$ (mV/m)")
    
    s.change_axes_color(ax1, line)
    

    return ax


def plot_aroural(ax, infile):

    ae = load(infile + "kyoto2013_03.txt")
    
    ax.plot(ae[["AE", "AL"]], 
               label = ['AE', 'AL'])
    
    ax.set(ylabel = 'AE/AL (nT)', 
              ylim = [-3000, 3000])
    
    ax.legend(ncol = 2, loc = 'upper right')
    
def plot_dst(ax, infile):
    dst = load(infile + "kyoto2000.txt")
    
    dst = dst.loc[
        (dst.index > dt.datetime(2013, 3, 16, 7)) &
        (dst.index < dt.datetime(2013, 3, 19, 16))]
    
    ax.plot(dst['dst'])
    
    ax.set(
        xlim = [dst.index[0], dst.index[-1]], 
        ylim = [-150, 70],
        ylabel = "Dst (nT)"
        )
    
    
    return dst



def plot_vz(ax):
    infile = "database/Digisonde/SAA0K_20130216_freq.txt"
    
    df = load(infile)

    freqs = ['6', '7', '8']

    vz = dg.drift(df, sel_columns = freqs)
    
    vz['avg'] = smooth2(vz['avg'], 5)
    ax.plot(vz['avg'], label = 'Disturbed days')
    
    def repeat():
        out1 = []
        for day in [16, 17, 18]:
            ds = pd.read_csv("mean.txt", index_col = 0)
            out = []
            for dn in ds.index:
                hour, minute = split_time(dn)
                if hour >= 24: hour - 24
                out.append(dt.datetime(2013, 3, day, hour, minute))
            ds.index = out
            out1.append(ds)
        
        return pd.concat(out1)
    
    ds = repeat()
    
    ax.plot(ds, color = 'red', label = "Quiet days")
    
    ax.legend(ncol = 4)
    
    ax.set(ylim = [-30, 50], ylabel = "$V_z$ (m/s)")
        
    
def plot_winds(ax):
    infile = "database/FabryPerot/2012/"
    paths = ['database/FabryPerot/2012/minime01_car_20130316.cedar.005.txt', 
             'database/FabryPerot/2012/minime01_car_20130317.cedar.005.txt', 
             'database/FabryPerot/2012/minime01_car_20130318.cedar.005.txt']
    
    # paths = ['database/FabryPerot/caj/minime02_caj_20130317.cedar.005.hdf5.txt', 
    #          'database/FabryPerot/caj/minime02_caj_20130316.cedar.005.hdf5.txt']
    
    for filename in paths:
      
        df = fp.FPI(filename).wind
        
        colors = ['k', '#0C5DA5']
        markers = ['s', '^']
        for i, col in enumerate(['north', 'south']):
            ds = df.loc[df['dir'] == col, 'vnu']
            
            ax.plot(ds, 
                    marker = markers[i], 
                    fillstyle = 'none',
                    label = col, 
                    color = colors[i])
            
    
    ax.set(
        ylim = [-70, 100], 
        ylabel = 'Meridional wind (m/s)'
        )
    
    ax.legend(['north', 'south'],
              ncol = 3, 
              loc = 'upper right')
    
    
   
    
def plot_indices_2():
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (14, 14),
        sharex = True,
        nrows = 5
        )
    
    plt.subplots_adjust(hspace = 0)
    
    infile = 'database/PlanetaryIndices/'
    
    plot_aroural(ax[1], infile)
    plot_mag_electron(ax[2], infile)
    plot_vz(ax[3])
    plot_winds(ax[4])
    
    
    df = load('database/HWM/winds_caj.txt')
    
    wd = df.loc[df['alt'] == 300, 'mer']
    
    ax[4].plot(wd, label = "HWM-14", color = 'red')
    df = plot_dst(ax[0], infile)
    ax[4].set(xlim = [df.index[0], df.index[-1]])
    s.format_time_axes(ax[4], pad = 60)
    
    for i, ax in enumerate(ax.flat):
        letter = s.chars()[i]
        ax.axhline(0, linestyle = '--')
        ax.text(
            0.02, 0.83, f"({letter})", 
            transform = ax.transAxes
            )
        plot_terminators(ax, df)
    return fig 

# f = plot_indices_2()
# 
# f.savefig('PlanetaryIndices/figures/IMF_index.png', dpi = 300)
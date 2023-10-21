import matplotlib.pyplot as plt
import FabryPerot as fp
import os
import base as s
import datetime as dt
from astropy.timeseries import LombScargle
from scipy.signal import find_peaks
import numpy as np 
import pandas as pd 
from scipy import signal

def get_dn(wd):
    return dt.datetime(
        wd.index[0].year, 
        wd.index[0].month, 
        wd.index[0].day, 
        21, 
        0)

def fs(timestamps):

    time_intervals = np.diff(timestamps)
    
    # Calculate the mean time interval to estimate fs
    mean_time_interval = np.mean(time_intervals)
    
    # Calculate the sampling frequency (fs) as the inverse of the mean time interval
    return 1 / mean_time_interval

def dtrend(ds, fs):

    avg = ds.rolling('1H').mean(center = True)
    
    ds['dtrend'] = ds - avg
    
    y = ds['dtrend'].values
    
    lowcut = 1 / 5
    highcut = 1 / 1.5


    nyquist = 0.5 * fs
    lowcut_normalized = lowcut #/ nyquist
    highcut_normalized = highcut #/ nyquist

    # Design the filter using scipy.signal
    b, a = signal.butter(
        4, [lowcut_normalized, highcut_normalized], 
        btype='band')

    # Apply the filter to the data
    filtered_data = signal.lfilter(b, a, y)
    return filtered_data

def lomb_scargle(ax, t, y):
    
    ls = LombScargle(t, y)
    
    frequency, power = ls.autopower(
            minimum_frequency = 1 / 5,
            maximum_frequency = 1 / 1.5,
            samples_per_peak = 100
            )
        
    period = 1 / frequency
    
    points = find_peaks(power, height = 0.01)
    
    ax.plot(period, power)
    for i in points[0]:
        
        ax.scatter(period[i], power[i])
 
    
def plot_directions(
        ax, 
        path, 
        site = 'car'
        ):
    
    wd = fp.FPI(path).wind
    tp = fp.FPI(path).temp
            
    # coords = {
    #     "zon": ("east", "west"), 
    #     "mer": ("north", "south")
    #     }
    
    coords = ["east", "west", "north", "south"]
    
    for coord in coords:
    
        ds = wd.loc[(wd["dir"] == coord)]
        
        ax[0, 0].errorbar(
            ds.index, 
            ds['vnu'], 
            yerr = ds["dvnu"], 
            label = coord, 
            capsize = 5
            )
        
        t = ds['time'].values
        y = dtrend(ds['vnu'], fs(t))
        
        
        ax[0, 1].plot(t, y)
        
        lomb_scargle(ax[0, 2], t, y)
        
        ds = tp.loc[(tp["dir"] == coord)]
        
        ax[1, 0].errorbar(
            ds.index, 
            ds['tn'], 
            yerr = ds['dtn'], 
            label = coord, 
            capsize = 5
            )
        
        t = ds['time'].values
        y = dtrend(ds['tn'], fs(t))
        
        ax[1, 1].plot(t, y)
        
        
        lomb_scargle(ax[1, 2], t, y)
        
       
        
    ax[0, 0].legend(
        ncol = 4, 
        loc = "upper center",
        bbox_to_anchor = (1.3, 1.2)
        )
      
        
    ax[0, 0].set(
        ylabel = "Velocidade (m/s)", 
        ylim = [-100, 150]
        )
    
    # ax[0, 1].set(
    #     ylabel = "Velocidade (m/s)", 
    #     ylim = [-60, 60]
    #     )
    
    ax[1, 0].set(
        ylabel = "Temperatura (K)", 
        ylim = [600, 1200])
    
    # ax[1, 1].set(
    #     xlabel = 'Universal time',
    #     ylabel = "Temperatura (K)", 
    #     ylim = [-60, 60]
    #     )
    
    ax[1, 2].set(
        xlabel = 'period',
        ylabel = "PSD"
        )

    ax[0, 0].axhline(0, color = "k", linestyle = "--")
    
    ax[0, 1].axhline(0, color = "k", linestyle = "--")
    ax[1, 1].axhline(0, color = "k", linestyle = "--")

    
    s.format_time_axes(
            ax[1, 0], hour_locator = 1, 
            day_locator = 1, 
            tz = "UTC"
            )
    
    dn = pd.to_datetime(wd.index.date[0])
    
    ds = fp.get_similar()
 
    df = ds.loc[ds.index == dn]

    for i, coord in enumerate(['vnu', 'tn']):
        for vls in df[coord].values:
            ax[i, 2].axvline(vls)
    


def plot_nighttime_observation(
        path, 
        ):
    
    fig, ax = plt.subplots(
        nrows = 2, 
        ncols = 3,
        figsize = (20, 10), 
        sharex =  'col', 
        dpi = 300
        )
    
    plt.subplots_adjust(
        wspace = 0.2, 
        hspace = 0.1
        )
    
    if "car" in path:    
        title = "Cariri"
        site = 'car'
    else:
        title = "Cajazeiras"
        site = 'car'
    plot_directions(ax, path, site = site)
        
    fig.suptitle(title)
    return fig
        

    
path = "database/FabryPerot/cariri/2013/"

path = 'database/FabryPerot/cariri/2013/minime01_car_20130422.cedar.005.txt'

# ds = fp.get_similar()
# save_in = 'database/img_fpi/'
# dates = np.unique(ds.index.date)
# dates = [dn.strftime('%Y%m%d') for dn in dates]


# for dn in dates: #:
    
#     for f in os.listdir(path):
#         if dn in f:

#             fig = plot_nighttime_observation(
#                 os.path.join(path, f)
#                 )
            
#             fig.savefig(save_in + dn, dpi = 400)




d = plot_nighttime_observation(path)
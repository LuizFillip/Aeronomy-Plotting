import PlasmaBubbles as pb
import matplotlib.pyplot as plt 
import numpy as np 
import base as b 
import datetime as dt 
from geophysical_indices import INDEX_PATH


def get_flux(dn):
    
    ip = b.load(INDEX_PATH)
    
    flux = b.get_value_from_dn(ip['f107a'], dn)
    return round(flux, 2)

b.config_labels()


args = dict(
    marker = 'o', 
    markersize = 1,
    linestyle = 'none', 
    color = 'k'
    )

def plot_roti_avg(ax, df):
    
   
    

    ax.plot(df['roti'], **args)
    ax.plot(df['avg'], lw = 3, color = 'r')
    b.format_time_axes(ax)
    
        
    ax.set(
        title = 'Obtaining the threshold', 
        yticks = np.arange(0, 5, 1), 
        ylabel = 'ROTI (TECU/min)',
        ylim = [0, 4], 
        xlim = [df.index[0], df.index[-1]]
        )
    
    
    return ax


def plot_std_shade(ax, df, i = 3):
    
    ax.fill_between(
        df.index, 
        df['avg'] + i * df['std'], 
        df['avg'] - i * df['std'], 
        alpha = 0.3, 
        color = 'r'
        )
    

def plot_base(ax, df):
    base = df['roti'].mean()
    ax.axhline(base, lw = 3, color = 'b')


def plot_threshold(ax, dn, lon = -60):

    threshold = pb.threshold(dn, lon)
    
    ax.axhline(
        threshold, 
        lw = 3, 
        color = 'magenta',
        label = f'{threshold} TECU/min'
        )

def plot_solar_flux(ax, dn):
    
    flux = get_flux(dn)
    
    ax.axhline(
        flux / 100, 
        lw = 3, 
        color = 'g', 
        label = f'{flux} sfu'
        )



def load_data(dn, long, N = 60):
    
    df = pb.longitude_sector(
        pb.concat_files(dn), long
        )
    
    df = b.sel_times(df, dn, hours = 11)
    
    df['avg'] =  b.smooth2(b.running(df['roti'], N), N * 4)
    df['std'] =  b.smooth2(b.running_std(df['roti'], N), N * 4)
    

    return df




def plot_get_thresholds_demo(dn, lon):
    
    fig, ax = plt.subplots(
        dpi = 300,
        sharex = True, 
        sharey = True,
        figsize = (12, 4)
        )
    
    df = load_data(dn, lon)
    
    plot_roti_avg(ax, df)
    plot_threshold(ax, dn, lon)
    plot_solar_flux(ax, dn)
    plot_base(ax, df)
    
    
    ax.legend()

    return fig

dn = dt.datetime(2015, 2, 17, 21)

lon = -60

f = plot_get_thresholds_demo(dn, lon)
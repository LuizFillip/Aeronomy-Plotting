import PlasmaBubbles as pb
import matplotlib.pyplot as plt 
import numpy as np 
import base as b 
import datetime as dt 

def get_flux(dn):
    
    ip = b.load(pb.INDEX_PATH)
    
    flux = pb.get_value_from_dn(ip['f107a'], dn)
    return round(flux, 2)

b.config_labels()

def plot_get_thresholds_demo(df):
    
    fig, ax = plt.subplots(
        dpi = 300,
        sharex = True, 
        sharey = True,
        figsize = (12, 4)
        )
    
    args = dict(
        marker = 'o', 
        markersize = 1,
        linestyle = 'none', 
        color = 'k'
        )
    

    ax.plot(df['roti'], **args)
    
    b.format_time_axes(ax)
    
        
    ax.set(
        title = 'Obtaining the threshold', 
        yticks = np.arange(0, 4, 1), 
        ylim = [0, 3], 
        xlim = [df.index[0], df.index[-1]]
        )
    
    
    return ax
    
    
def plot_elements(ax, df):
    # ds = df.rolling('60min').agg('mean')
    avg = b.running(df['roti'], N = 60)
    
    ax.plot(df.index, avg, color = 'r', lw = 3)
    base = df['roti'].mean()
    ax.axhline(base, lw = 3, color = 'b')
    flux = get_flux(dn)
    threshold = pb.set_value(
        avg.max(), flux)
    ax.axhline(threshold, 
                lw = 3, color = 'magenta',
                label = f'{threshold} TECU/min')
    
    ax.axhline(flux / 100, lw = 3, color = 'g', 
                label = f'{flux} sfu')
    
    ax.legend()


dn = dt.datetime(2015, 2, 17, 21)


df = pb.longitude_sector(
    pb.concat_files(dn), -60
    )

df = b.sel_times(df, dn, hours = 9)

ax = plot_get_thresholds_demo(df)

N = 60
df['avg'] =  b.smooth2(b.running(df['roti'], N), N * 4)
df['std'] =  b.smooth2(b.running_std(df['roti'], N), N * 4)

ax.plot(df['avg'], lw = 3, color = 'r')

i = 2

ax.fill_between(
    df.index, 
    df['avg'] + i * df['std'], 
    df['avg'] - i * df['std'], 
    alpha = 0.3, 
    color = 'r'
    )


# ds = df.rolling('60min').agg('mean')

# ax.plot(ds['roti'], lw = 3, color = 'g')


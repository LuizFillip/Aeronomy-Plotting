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

dn = dt.datetime(2015, 2, 18, 3)


df = pb.longitude_sector(
    pb.concat_files(dn), -80
    )

df = b.sel_times(df, dn, hours = 11)

base = df['roti'].mean()

ax.plot(df['roti'], **args)

ds = df.rolling('60min').agg('mean')

ax.plot(ds, color = 'r', lw = 3)

ax.axhline(base, lw = 3, color = 'b')


flux = get_flux(dn)
ax.axhline(flux / 100, lw = 3, color = 'g', 
           label = f'{flux} sfu')

b.format_time_axes(ax)

title = 'Obtaining the threshold'

threshold = pb.set_value(
    ds['roti'].max(), flux, base.max())

ax.axhline(threshold, 
           lw = 3, color = 'magenta',
           label = f'{threshold} TECU/min')

ax.legend()

ax.set(
    title = title, 
    yticks = np.arange(0, 4, 1), 
    ylim = [0, 3], 
    xlim = [df.index[0], df.index[-1]]
    )


plt.show()
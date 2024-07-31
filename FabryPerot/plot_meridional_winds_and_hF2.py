import matplotlib.pyplot as plt
import base as b 
import GEO as gg 
import datetime as dt 
import numpy as np
import core as c 
import plotting as pl 
import digisonde as dg 
import FabryPerot as fp


fig, ax = plt.subplots(
    dpi = 300, 
    figsize = (12, 10), 
    nrows = 2, 
    sharex = True
    )

plt.subplots_adjust()
site = 'SAA0K'
# site = 'FZA0M'
cols = list(range(4, 8, 1))
dn = dt.datetime(2022, 7, 24)
fn  = f'{site}_{dn}.TXT'
 
file = dn.strftime(f'{site}_%Y%m%d(%j).TXT')
 
df = dg.IonoChar(file, cols, sel_from = 17)

ax[0].plot(df.chars['hF2']) 
ax[0].set(ylabel = 'hF2 (km)')

path = 'database/FabryPerot/cj/bfp220724g.7100.txt'

wd = fp.FPI(path).wind



for row, direction in enumerate(['north', 'south']):
    # print(col, dirs)
    ds = wd.loc[(wd["dir"] == direction)]
    
    ax[1].errorbar(
        ds.index, 
        ds['vnu'], 
        yerr = ds["dvnu"], 
        label = direction, 
        capsize = 5
            )

ax[1].set(ylabel = 'Vento meridional (m/s)')
b.format_time_axes(ax[-1])
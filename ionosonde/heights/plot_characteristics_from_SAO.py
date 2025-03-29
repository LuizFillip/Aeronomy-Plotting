
import matplotlib.pyplot as plt 
import digisonde as dg 
import datetime as dt 
import base as b 

infile = 'digisonde/data/SAO/chars/'

dn = dt.datetime(2023, 10, 14)

sites = ['FZA0M'] #, 'SAA0K', 'BVJ03', 'BLJ03']

site = sites[0]





fig, ax = plt.subplots(
    nrows = 2,
    figsize = (15, 8)
    )

for i, site in enumerate(sites):
     

    ds = dg.chars(infile + dg.dn2fn(dn, site))
    
    # ds['hmF2'] = b.smooth2(ds['hmF2'], 2)
    # ds['foF2'] = b.smooth2(ds['foF2'], 2)
    
    ax[0].plot(ds.index, ds['foF2'], label = site)
    ax[1].plot(ds.index, ds['hmF2'], label = site)
    
    d = dt.timedelta(hours = 12)
    
    ax[-1].set(xlim = [ds.index[0] + d, ds.index[-1]])
    
b.format_time_axes(ax[-1], translate = True, pad = 80)

ax[-1].legend()
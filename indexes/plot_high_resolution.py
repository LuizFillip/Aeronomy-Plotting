import base as b 
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import plotting as pl 

infile = 'database/indices/omni_high/2015'
df = b.load(infile)

df = df.loc[df['by'] < 1000]

dn = dt.datetime(2015, 12, 21)


ds = b.range_dates(df, dn, days = 2)




fig, ax = plt.subplots(
    dpi = 300,
    figsize = (14, 14), 
    nrows = 4, 
    sharex = True
    )

plt.subplots_adjust(hspace = 0.05)


pl.plot_magnetic_fields(ax[0], ds)

b.format_time_axes(ax[-1], hour_locator = 12, pad = 80)
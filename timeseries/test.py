import matplotlib.pyplot as plt
import GNSS as gs
import base as b
import datetime as dt
import numpy as np

year = 2021

doy = gs.doy_from_date(dt.date(year, 1, 1))
path = gs.paths(year, doy)
ds = b.load(path.fn_roti)


ds = gs.filter_bad_prns(ds, path)

ds[ds['roti'] > 1]

df = ds.loc[(ds['sts'] == 'ceft') &
            (ds['prn'] == 'R15') ]


fig, ax = plt.subplots()

dn = dt.datetime(year, 1, 1, 0)
df = b.sel_times(df, dn, hours = 4)

df['roti'].plot()
avg = np.gradient(df['roti'])
ax.plot(df.index, avg)
ax.set(ylim = [0, 5])

avg
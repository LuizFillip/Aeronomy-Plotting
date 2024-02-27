import base as b 
import datetime as dt 
import pandas as pd
import matplotlib.pyplot as plt 


infile = 'digisonde/data/chars.txt'

dn = dt.datetime(2013, 1, 1, 20)
ds = b.load(infile)

ds['doy'] =  ds.index.day_of_year
ds['year'] = ds.index.year

col = 'QF'

ds[col] =  b.smooth2(ds[col], 6)


df = pd.pivot_table(
    ds, 
    values = col, 
    columns = 'year', 
    index = 'doy'
    )


df = df.interpolate()

plt.contourf(df.columns, df.index, df.values, 20)
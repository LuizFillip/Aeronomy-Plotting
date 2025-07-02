import base as b 
import pandas as pd 
import datetime as dt 

infile = 'plotting/FabryPerot/December2015'

df = b.load(infile)


# df["time"] = b.time2float(df.index.time)

# ds = pd.pivot_table(
#     df, 
#     columns = df.index.date, 
#     index = "time", 
#     values = "zon"
#     )

# ds.mean(axis = 1).plot()

start = dt.datetime(2015, 12, 19)
end = dt.datetime(2015, 12, 23)

ds = b.sel_dates(df, start, end)

ds['ON2'] = ds['O'] / ds['N2']

# ds['O'].plot()
ds['ON2'].plot()

3.7e−12*(250/Te)
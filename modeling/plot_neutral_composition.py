import base as b 
import datetime as dt 
import pandas as pd
import matplotlib.pyplot as plt 
import core as c 

df = b.load('models/temp/msis_saa_300')

df = df.loc[df.index.time == dt.time(22, 0)]

df.index = df.index.to_series().apply(lambda n: n.replace(hour = 0))

df['N2O2'] = df['O'] / df['N2']

df = df.resample('27D').mean()

# df.loc[df.index.year == 2015]
df['N2O2'].plot()



# df['day'] = df.index.year + df.index.day_of_year / 365
# df['month'] = df.index.month

# ds = pd.pivot_table(
#     df, 
#     columns = 'month', 
#     index = 'day', 
#     values = 'N2O2'
#     )


# ds.mean()


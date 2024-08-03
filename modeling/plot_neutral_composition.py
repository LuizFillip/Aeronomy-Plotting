import base as b 
import datetime as dt 
import pandas as pd
import matplotlib.pyplot as plt 
import core as c 

def plot_neutral_composition(ax):
    import GEO as gg 
    
    df = b.load('models/temp/msis_saa_300')
    
    df = df.loc[(df.index.time == dt.time(22, 0)) &
                (df.index.year  < 2023)]
    
    df.index = df.index.to_series().apply(
        lambda n: n.replace(hour = 0))
    
    df['N2O2'] = df['O'] / df['N2']
    
    df = df.resample('1M').mean()
    
    mar = df.loc[df.index.month == 3]
    mar.index = mar.index.map(gg.year_fraction)
    
    sep = df.loc[df.index.month == 9]
    sep.index = sep.index.map(gg.year_fraction)
    
    df.index = df.index.map(gg.year_fraction)
    # df.loc[df.index.year == 2015]
    ax.plot(df['N2O2'], lw = 2)
    ax.scatter(mar.index, mar['N2O2'], s = 50, c = 'k')
    ax.scatter(sep.index, sep['N2O2'], s = 50, c = 'b')
    ax.set(ylabel = '$n(O) / n(N_2)$',
           ylim = [2, 10])
    
    return None 


df = b.load('models/temp/msis_saa_300')

df = df.loc[(df.index.time == dt.time(22, 0)) &
            (df.index.year  < 2023)]

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


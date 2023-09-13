import base as b 
import datetime as dt

import matplotlib.pyplot as plt
import PlasmaBubbles as pb 

b.config_labels()



def threshold(df, percent = 0.8):
    
    ds = df.rolling('1H').mean(
        center = True)
    
    vmax = ds.max() 
    vavg = ds.mean() 
        
    value = ((vmax + vavg) / 2 ) * percent
    
    if value < vavg:
        return (vmax + vavg) * (1 + percent)
    else:
        return value
    
    
def plot_thresholds_example(ax, df):
    
    
    ax.plot(df)
    ax.plot(df.rolling('1H').mean())
    
    val = threshold(df)
    ax.axhline(
        val, 
        lw = 2, 
        color = 'r', 
        label = f'Threshold = {round(val, 1)} TECU/min'
        )
    
    ax.legend()
    if val < 1:
        ax.set(ylim = [0, 1])
    else:
        ax.set(ylim = [0, 5])
        
        

year = 2013
df = b.load(f'database/epbs/longs/{year}.txt')


dn = dt.datetime(year, 1, 1, 20)
df = b.sel_times(df, dn, hours = 11)



    
fig, ax = plt.subplots(
    figsize = (10, 6), 
    dpi = 300,
    nrows = 2,
    sharex = True,
    sharey = True,
    )

for i, col in enumerate(['-40', '-50']):
    
    plot_thresholds_example(ax[i], df[col])
    
    ax[i].set(title = f'Longitude = {col}° ({year})')

b.format_time_axes(ax[1])


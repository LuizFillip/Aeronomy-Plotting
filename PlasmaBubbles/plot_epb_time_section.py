import matplotlib.pyplot as plt
import base as b 
import pandas as pd 
import numpy as np
import datetime as dt 
import GEO as gg 

b.config_labels()


def plot_epb_time_section():
    
    return 

def shade_area(
        ax, 
        start,
        offset = 2,
        name = 'Daytime', 
        color = '#0C5DA5'
        ):

    end = start + dt.timedelta(hours = offset)
    
    ax.axvspan(
        start, end, 
        ymin = 0, ymax = 1,
        alpha = 0.2, 
        color = color
        )
    
    delta = dt.timedelta(hours = 1.)
    middle = start + (end - start) / 2 
    
    ax.text(
        middle - delta, 
        0.5, 
        name, 
        transform = ax.transData
        )



def dumb_data(start):
    
    end = start + dt.timedelta(hours = 11)
    time = pd.date_range(start, end, freq = '1min')
    return pd.DataFrame({'Occ': np.zeros(len(time))}, index = time)

dn = dt.datetime(2013, 12, 24, 21)
df = dumb_data(dn)


fig, ax = plt.subplots(
    figsize = (12, 6),
    dpi = 300
    )


ax.plot(df)

terminator = gg.terminator(-50, dn, float_fmt = False)

shade_area(
        ax, 
        terminator,
        name = 'Post-sunset', 
        color = '#0C5DA5'
        )


shade_area(
        ax, 
        terminator + dt.timedelta(hours = 2),
        offset = 8, 
        name = 'Post-midnight', 
        color = 'lightgray'
        )
 
ax.axvline(terminator, color = 'k', lw = 2, label = 'Solar terminator (300 km)')
midnight = dt.datetime(2013, 12, 25, 3)
ax.axvline(midnight, 
           color = 'k', lw = 2, 
           linestyle = '--')
ax.text(terminator, 1.15,
    'Solar terminator (300 km)',
    transform = ax.transData
    )



ax.text(midnight, 1.15,
    'Local midnight',
    transform = ax.transData
    )

ax.set(
       ylabel = 'Occurrence',
       ylim = [-0.1, 1.1],
       yticks = [0, 1]
       )

for line in [0,1]:
    
    ax.axhline(line, linestyle = '--')

fig.suptitle('São Luis', y = 1.05)
b.format_time_axes(ax)

plt.show()
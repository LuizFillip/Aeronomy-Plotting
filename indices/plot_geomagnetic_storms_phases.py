import base as b
import core as c
import datetime as dt 
import matplotlib.pyplot as plt 
import GEO as gg 
import numpy as np 

PATH = 'database/indices/omni_hourly.txt'


# dn = dt.datetime(2015, 3, 17 )


def plot_geomagnetic_storms_phases( df1):
    
    
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (10, 4)
        )
    
    ax.plot(df1['dst'])
    
    # ax.axvline(ds.loc[dn, 'main'])
    
    # for col in ['main', 'end', 'start']:    
    #     ax.axvline(ds.loc[dn, col], lw = 2)
    
    
    ax.axhline(0, linestyle = '--')
    ax.axhline(-30, linestyle = '--')
    
    ax.set(
        xlim = [df1.index[0], df1.index[-1]],
        ylim = [-200, 50], 
        xlabel = 'Days',
        ylabel = 'Dst (nT)'
        )
    
    # for long in np.arange(-80, -40, 10)[::-1]:
    #     dusk = gg.terminator(
    #         long, 
    #         ds.index[0], 
    #         float_fmt = False
    #         )
    
    #     ax.axvline(dusk, lw = 1, linestyle = '-')
    
    b.format_days_axes(ax, day_locator = 10,  second_axes = True)
    
    return fig 


# dn = ds.index[1]
df = b.load(PATH)

dn = dt.datetime(2022, 1, 1)    
end = dn + dt.timedelta(days = 120)

# end = ds.loc[dn, 'end']
# start = ds.loc[dn, 'start']
    
    
df1 = b.sel_dates(
      df, 
      dn, 
      end 
      )
 
# ds = c.find_storms(df1)

fig = plot_geomagnetic_storms_phases(df1)


# df1 
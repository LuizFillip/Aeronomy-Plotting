import matplotlib.pyplot as plt
import datetime as dt 
import core as c 
import base as b




df = b.load('database/longitudes_all_years.txt')


s = dt.datetime(2013, 3, 14, 20)
e = dt.datetime(2013, 3, 20, 8)
ds = b.sel_dates(df, s, e)

b.config_labels()
ds1 = c.gamma(time = None)

fig, ax = plt.subplots(
       dpi = 300, 
       nrows = 2, 
       figsize = (12, 8), 
       sharex = True 
       )

plt.subplots_adjust(hspace = 0.1)
ds1 = b.sel_dates(ds1, s, e )

color = 'k'
ax[0].plot(ds1['gamma'], color = color)

ax[1].plot(ds['-50'], color = color)


points = ds1.loc[ds1.index.time == dt.time(22, 0)]
x = points.index.values
y = points.gamma.values
ax[0].scatter(x, y, c = 'r')

ax[0].set(ylim = [0, 3], 
          ylabel = '$\\gamma_{RT}~(10^{-3}s^{-1})$')

b.format_days_axes(ax[1])
ax[1].set(ylim = [0, 2], 
          ylabel = 'ROTI (TECU/min)', 
          xlabel = 'Days')


for i, line in enumerate([max(y), min(y)]):
    
    ax[0].axhline(line, color = color)
    
    # b.dark_background(
    #         fig, 
    #         ax[i], 
    #         background_col = 'xkcd:black', 
    #         face_col = (0.06, 0.06, 0.06)
    #         )


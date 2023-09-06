from events import probability_distribuition
import matplotlib.pyplot as plt 
import base as b

fig, ax = plt.subplots(
    dpi = 300,
    ncols = 2, 
    nrows = 2,
    sharex = True,
    sharey = True,
    figsize = (10, 10)
    )

plt.subplots_adjust(wspace = 0.1)

df = b.load('all_results.txt')

df = df.loc[df['kp_max'] > 4]



df['doy'] = df.index.day_of_year 
seasons = [summer(df), fall(df), winter(df), spring(df)]
names = ['summer', 'fall', 'winter', 'spring']


for i, ax  in enumerate(ax.flat):

    ds = probability_distribuition(
            seasons[i],
            step = 0.2, 
            col_gama = 'all',
            col_epbs = 'epb'
            )
    
    ax.plot(ds['start'], ds['rate'])
    ax.set(xlim = [0, 3], 
           ylim = [-20, 120],
           title = names[i],
           )
    
    if i >= 2:
        ax.set(xlabel = '$\\gamma_{FT}~\\times 10^{-3}$ ($s^{-1}$)')
        
    if i == 0 or i == 2:
        ax.set(ylabel = 'EPBs probability \noccurrence ($\\%$)')
    
    
fig.suptitle('disturbed days ($kp > 4$)')
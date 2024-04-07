import matplotlib.pyplot as plt
import base as b
import core as c 
import plotting as pl 

fig, ax = plt.subplots(
     dpi = 300, 
     nrows = 2,
     sharex = True,
     figsize = (12, 12)
     )
 
plt.subplots_adjust(hspace = 0.05)

ds = c.load_results('saa', eyear = 2022)

translate = True 
outliner = 10
label = ''
parameter = 'gamma'
ds = ds.loc[(ds['f107a'] > 84) & (ds['kp'] > 3)]
data, epbs = pl.plot_distribution(
        ax[0], 
        ds,
        parameter = parameter,
        label = label,
        axis_label = True,
        outliner = outliner, 
        translate = translate,
        limit = True,
        ylim = [0.1, 1.1]
    )

def plot_epbs_number(ax, data):
    for x, y, z in data[['start', 'rate', 'epbs']].values:
        
        ax.text(x - 0.05, (y *100) + 5, int(z), transform = ax.transData)
        
plot_epbs_number(ax[0], data)

index = 0

days = pl.plot_histogram(
         ax[1], 
         data, 
         index, 
         label, 
         parameter = parameter,
         axis_label = True,
         translate = translate
     )
 
ax[1].set(ylim = [0, 800], xlim = [-0.1, 2.8])
ax[0].set(xlabel = '')

def plot_epbs_number(ax, data):
    for x, y in data[['start', 'days']].values:
        
        ax.text(x - 0.05, (y) + 5, int(y), transform = ax.transData)
        
plot_epbs_number(ax[1], data)
# total_epb.append(epbs)
# total_day.append(days)
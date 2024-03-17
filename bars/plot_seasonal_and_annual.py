import matplotlib.pyplot as plt
import base as b 
import core as c 
import PlasmaBubbles as pb 


args = dict(
    edgecolor = 'black', 
    color = 'gray', 
    linewidth = 1
    )

b.config_labels()







def plot_annual_seasonal(ds):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        sharey = True,
        ncols = 2,
        figsize = (16, 4)
        )
    
    plt.subplots_adjust(wspace = 0.05)
    
    
    return fig 


def format_days_axes(ax):
    
    major_formatter = dates.DateFormatter('%Y')
    major_locator = dates.YearLocator()
    
    
    ax.xaxis.set_major_locator(major_locator)
    ax.xaxis.set_major_formatter(major_formatter)
    
    ax.set(xlabel = 'Anos', 
    xlim = [df.index[0], df.index[-1]])
    

# ds = ev.epbs(
#         col = -50, 
#         class_epb = 'midnight',
#         geo = False
#         )



df = b.load('events_2013_2023_2')

ds = pb.sel_sunset(df)


import matplotlib.dates as dates


fig, ax = plt.subplots(
    dpi = 300, 
    sharey = True,
    figsize = (16, 6)
    )

df  = c.seasonal_yearly_occurrence(ds, col = -50)


ax.bar(df.index, df.values.ravel(), width = 20, **args)
    


    
    
format_days_axes(ax)

ax.set(
    ylabel = 'Noites com EPB',
    ylim = [0, 35]
    )

plt.xticks(rotation = 0)

plt.show()


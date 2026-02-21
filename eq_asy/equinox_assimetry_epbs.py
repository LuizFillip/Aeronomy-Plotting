import base as b
import pandas as pd 
import core as c 
import matplotlib.pyplot as plt 
import numpy as np 
import matplotlib.gridspec as gridspec

def join_data_pipe():
    infile = 'database/epbs/north/'
    out = []
    for year in range(2010, 2024):
        path = f'{infile}{year}'
        out.append(b.load(path))
        
    df = pd.concat(out).sort_index()
    
    df = df.loc[~(df['duration'] < 0.2)]
    
    df['lon'] = -50
    
    return df
    





 
def plot_f107(ax):
    PATH_INDEX =  'database/indices/omni_pro2.txt'
    ds = b.load(PATH_INDEX)
     
    ds["f107a"] = ds["f107"].rolling(window = 81).mean()
     
    ax1 = ax.twinx()
    
    ax1.plot(
        ds['f107'],
        lw = 1, 
        color = 'w'
        )
    
    ax1.set(
            ylabel = 'F10.7 (sfu)',
            ylim = [60, 400], 
            
            )
    
    return 

def plot_contour_roti(ax, start, end,  vmax = 5):
    df = b.load('maximums_roti')
    df['date'] = pd.to_datetime(df['date'])
    df = df.loc[
        (df['date'].dt.year >= start) & 
        (df['date'].dt.year <= end) 
        ]
    ds = df.pivot(
        index = 'time', 
        columns = 'date', 
        values = '-50'
        ) 
    values =  ds.values
   
    values = np.where(values > vmax, vmax, values)
    
    img = ax.contourf(
        ds.columns, 
        ds.index, 
        values,
        levels = np.arange(0, vmax + 0.2, 0.2), 
        cmap = 'inferno'
        )
    
    ax.set(
        ylim = [20, 29.1],
        yticks = np.arange(20, 30, 2),
        ylabel = 'Universal Time', 
        xlim = [df['date'].min(), df['date'].max()],
        xlabel = 'Years'
        )
    
    ticks = np.arange(0, vmax + 1, 1)
    
    cax = ax.inset_axes([1.1, 0., 0.03, 1])

    cb = plt.colorbar(
        img, 
        cax = cax,
        ticks = ticks, 
        location = 'right'
        )
     
    cb.set_label('ROTI (TECU/min)')
    
    dates = pd.date_range(
        f'{start}-01-01', 
        f'{end}-01-01', freq = '1Y'
        )
    
    for dn in dates:
        ax.axvline(
            dn, 
            lw = 2, 
            color = 'w', 
            linestyle = '--'
            )
    
    plot_f107(ax)
    
    return None 
    

def plot_equinox_asymetry(ax, ds):
  
    bar_width = 0.2
    
    lbs = {'march': "black", 'september':  "purple"}
    
    for idx, (name, color) in enumerate(lbs.items()):
        
        data = ds[name]
        if idx == 0:
            offset = 0
        else:
            offset = (bar_width / idx)
        
        label = f'{name.capitalize()} Equinox'
        ax.bar(
               (ds.index - 0.1) + offset,
               data,
               width=bar_width,
               color= color,
               label= label,
               edgecolor = 'k'
           )
            
  
    ax.legend(
        loc = 'upper center',
        ncol = 2,  
        )
    
    ax.set(
        
        ylim = [0, 70],
        yticks = np.arange(0, 80, 20),
           ylabel = 'Occurrence rate (\%)'
           )
    
    
    return fig, ax

    
def data(start, end, percent = True):
    # df = join_data_pipe()
    df = b.load('database/epbs/epbs_2013_2023')
   
    df = c.add_geo(df, start, end)
    
    df = df.loc[df['kp'] <= 3]
    
    ds = c.pivot_epb_by_type(df, total = False, sel_lon = -50)
    
    return c.count_epbs_by_season(ds, start, end, percent = percent)
    
start, end = 2015, 2023
 
ds = data(start, end)

fig = plt.figure(
    figsize = (12, 8),
    dpi = 300
    )
gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1])
plt.subplots_adjust(hspace = 0.03)

ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])
 
ax1.tick_params(labelbottom=False)

plot_equinox_asymetry(ax1, ds)
plot_contour_roti(ax2, start, end)

# ax2.set(xticks = np.arange(start, end + 1, 1))

fig.align_ylabels()

axs = [ax1, ax2]

b.plot_letters(
        axs, 
        x = 0.02, 
        y = 0.8, 
        offset = 0, 
        fontsize = 30,
        num2white = 1
        )

plt.show()
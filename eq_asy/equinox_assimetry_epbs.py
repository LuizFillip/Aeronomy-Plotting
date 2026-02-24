import base as b
import pandas as pd 
import core as c 
import matplotlib.pyplot as plt 
import numpy as np 
import matplotlib.gridspec as gridspec


 
def plot_f107(ax, color = 'magenta'):
    PATH_INDEX =  'database/indices/omni_pro2.txt'
    ds = b.load(PATH_INDEX)
     
    ds["f107a"] = ds["f107"].rolling(window = 81).mean()
     
    ds.index = ds.index.year + (ds.index.day_of_year / 366 )
    
    
    ax1 = ax.twinx()
    
    ax1.plot(
        ds['f107'],
        lw = 1, 
        color = 'w'
        )
    
    ax1.set(
           
            yticks = np.arange(0, 400, 100),
            ylim = [60, 900], 
            )
    
    ax1.text(
        1.05, 0, 'F10.7 (sfu)', 
        fontsize = 15, 
        rotation = 'vertical',
        transform = ax1.transAxes
        )
    return 

def load_averages(time_start = 19):
    df = pd.read_csv(
        'database/epbs/pivot_cg',
        index_col = 0).interpolate()

    df.columns = pd.to_numeric(df.columns) 
     
    index =  np.arange(
        time_start , df.index.min(), 
        df.index[1]-df.index[0]
        )[:-1]
    
    data = np.zeros((len(index), len(df.columns)))
    
    df2 = pd.DataFrame(
        data, 
        columns = df.columns, 
        index = index
        )
    
    return pd.concat([df2, df]).sort_index().sort_index(axis=1)



def plot_contour_roti(ax, start, end, vmax = 3):
 
    df = load_averages()
 
    img = ax.pcolormesh(
        df.columns, 
        df.index, 
        df.values ,
        vmin = 0, 
        vmax = vmax, 
        cmap = 'inferno'
        )
    
    ax.set(
        ylim = [19, 30],
        yticks = np.arange(19, 30, 2),
        ylabel = 'Universal Time', 
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
 
    for dn in np.arange(2009, 2024):
        ax.axvline(
            dn, 
            lw = 1, 
            color = 'w', 
            linestyle = '--'
            )
    
    plot_f107(ax, color = 'w')
    
    # return None 
    

def plot_equinox_asymetry(ax, ds, bar_width = 0.2):
  
    lbs = {'march': "black", 'september':  "purple"}
    
    for idx, (name, color) in enumerate(lbs.items()):
        
        data = ds[name]
        if idx == 0:
            offset = 0
        else:
            offset = (bar_width / idx )
        
        label = f'{name.capitalize()} Equinox'
        ax.bar(
               (ds.index + 0.3) + offset,
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
        xlim = [2009, 2024],
        ylim = [0, 70],
        yticks = np.arange(0, 80, 20),
           ylabel = 'Occurrence rate (\%)'
           )
    
    
    return  

    
def data(start, end, percent = False):
 
    df = b.load('database/epbs/cg_2009_2023')
   
    df = c.add_geo(df, start, end)
    
    df = df.loc[df['kp'] <= 3]
    
    ds = c.pivot_epb_by_type(
        df, total = False, sel_lon = -50)
    
    return c.count_epbs_by_season(
        ds, start, end, percent = percent)

def plot_roti_and_bars(start = 2010, end = 2023):
    
    ds = data(start, end)
    
    fig = plt.figure(
        figsize = (12, 8),
        dpi = 300
        )
    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1])
    plt.subplots_adjust(hspace = 0.2)
    
    ax2 = fig.add_subplot(gs[0])
    ax1 = fig.add_subplot(gs[1], sharex = ax2)
    
     
    ax2.tick_params(labelbottom=False)
    
    plot_equinox_asymetry(ax1, ds)
    plot_contour_roti(ax2, start, end)
     
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
    
    path_to_save = 'G:\\Meu Drive\\Papers\\EquinoxAsymetry\\'
     
    figname = 'roti_and_bars'
    # fig.savefig(path_to_save + figname, dpi = 400)

plot_roti_and_bars(start = 2009)


